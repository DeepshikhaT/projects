#!/usr/bin/env python3
"""
Ansible Automation API Server
==============================
Flask REST API to trigger Ansible playbooks programmatically

Author: Deepshikha Tripathi
Purpose: Enable API-driven network automation

Usage:
    python ansible_api.py

API Endpoints:
    POST /api/vlans/configure      - Configure VLANs
    POST /api/ospf/configure       - Configure OSPF routing
    POST /api/backup/configs       - Backup device configurations
    POST /api/health/check         - Run network health check
    GET  /api/playbooks            - List available playbooks
    GET  /api/jobs/<job_id>        - Get job status
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json
import uuid
from datetime import datetime
import threading
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
BASE_DIR = Path(__file__).parent.parent
PLAYBOOKS_DIR = BASE_DIR / 'playbooks'
INVENTORY_DIR = BASE_DIR / 'inventory' / 'lab'
LOGS_DIR = BASE_DIR / 'logs' / 'api'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# In-memory job storage (in production, use Redis or database)
jobs = {}


class AnsibleRunner:
    """Class to execute Ansible playbooks"""

    def __init__(self, playbook, inventory='hosts', extra_vars=None, tags=None, limit=None):
        """
        Initialize Ansible runner

        Args:
            playbook: Name of playbook file
            inventory: Inventory file name
            extra_vars: Dictionary of extra variables
            tags: Comma-separated tags to run
            limit: Limit execution to specific hosts
        """
        self.playbook = PLAYBOOKS_DIR / playbook
        self.inventory = INVENTORY_DIR / inventory
        self.extra_vars = extra_vars or {}
        self.tags = tags
        self.limit = limit
        self.job_id = str(uuid.uuid4())

    def build_command(self):
        """Build ansible-playbook command"""
        cmd = [
            'ansible-playbook',
            str(self.playbook),
            '-i', str(self.inventory)
        ]

        # Add extra variables
        if self.extra_vars:
            cmd.extend(['-e', json.dumps(self.extra_vars)])

        # Add tags
        if self.tags:
            cmd.extend(['--tags', self.tags])

        # Add limit
        if self.limit:
            cmd.extend(['--limit', self.limit])

        # Add verbose mode for better output
        cmd.append('-v')

        return cmd

    def run(self):
        """Execute the playbook"""
        cmd = self.build_command()

        # Initialize job status
        jobs[self.job_id] = {
            'id': self.job_id,
            'status': 'running',
            'playbook': self.playbook.name,
            'started_at': datetime.now().isoformat(),
            'command': ' '.join(cmd),
            'output': '',
            'error': '',
            'return_code': None
        }

        try:
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=BASE_DIR
            )

            # Update job status
            jobs[self.job_id].update({
                'status': 'completed' if result.returncode == 0 else 'failed',
                'completed_at': datetime.now().isoformat(),
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            })

            # Save output to file
            log_file = LOGS_DIR / f"{self.job_id}.log"
            with open(log_file, 'w') as f:
                f.write(f"Command: {' '.join(cmd)}\n")
                f.write(f"Return Code: {result.returncode}\n")
                f.write(f"\nSTDOUT:\n{result.stdout}\n")
                f.write(f"\nSTDERR:\n{result.stderr}\n")

            return jobs[self.job_id]

        except subprocess.TimeoutExpired:
            jobs[self.job_id].update({
                'status': 'timeout',
                'completed_at': datetime.now().isoformat(),
                'error': 'Playbook execution timed out after 5 minutes'
            })
            return jobs[self.job_id]

        except Exception as e:
            jobs[self.job_id].update({
                'status': 'error',
                'completed_at': datetime.now().isoformat(),
                'error': str(e)
            })
            return jobs[self.job_id]

    def run_async(self):
        """Run playbook asynchronously in background thread"""
        thread = threading.Thread(target=self.run)
        thread.start()
        return self.job_id


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """API welcome page"""
    return jsonify({
        'message': 'Ansible Automation API',
        'version': '1.0',
        'endpoints': {
            'vlans': '/api/vlans/configure',
            'ospf': '/api/ospf/configure',
            'backup': '/api/backup/configs',
            'health': '/api/health/check',
            'playbooks': '/api/playbooks',
            'jobs': '/api/jobs/<job_id>'
        }
    })


@app.route('/api/playbooks', methods=['GET'])
def list_playbooks():
    """List all available playbooks"""
    playbooks = []

    for file in PLAYBOOKS_DIR.glob('*.yml'):
        playbooks.append({
            'name': file.name,
            'path': str(file.relative_to(BASE_DIR)),
            'size': file.stat().st_size,
            'modified': datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })

    return jsonify({
        'playbooks': playbooks,
        'count': len(playbooks)
    })


@app.route('/api/vlans/configure', methods=['POST'])
def configure_vlans():
    """
    Configure VLANs on switches

    Request Body:
    {
        "inventory": "hosts",          # Optional, default: hosts
        "limit": "switch1,switch2",    # Optional, limit to specific hosts
        "async": true                  # Optional, run asynchronously
    }

    Response:
    {
        "job_id": "uuid",
        "status": "running|completed",
        "message": "..."
    }
    """
    data = request.get_json() or {}

    inventory = data.get('inventory', 'hosts')
    limit = data.get('limit')
    run_async = data.get('async', False)

    runner = AnsibleRunner(
        playbook='configure_vlans.yml',
        inventory=inventory,
        limit=limit
    )

    if run_async:
        # Run in background
        job_id = runner.run_async()
        return jsonify({
            'job_id': job_id,
            'status': 'running',
            'message': 'VLAN configuration started in background',
            'check_status': f'/api/jobs/{job_id}'
        }), 202
    else:
        # Run synchronously
        result = runner.run()
        return jsonify(result), 200 if result['return_code'] == 0 else 500


@app.route('/api/ospf/configure', methods=['POST'])
def configure_ospf():
    """
    Configure OSPF routing on routers

    Request Body:
    {
        "inventory": "hosts",
        "limit": "router1,router2",
        "async": true
    }
    """
    data = request.get_json() or {}

    inventory = data.get('inventory', 'hosts')
    limit = data.get('limit')
    run_async = data.get('async', False)

    runner = AnsibleRunner(
        playbook='configure_ospf.yml',
        inventory=inventory,
        limit=limit
    )

    if run_async:
        job_id = runner.run_async()
        return jsonify({
            'job_id': job_id,
            'status': 'running',
            'message': 'OSPF configuration started in background',
            'check_status': f'/api/jobs/{job_id}'
        }), 202
    else:
        result = runner.run()
        return jsonify(result), 200 if result['return_code'] == 0 else 500


@app.route('/api/backup/configs', methods=['POST'])
def backup_configs():
    """
    Backup device configurations

    Request Body:
    {
        "inventory": "hosts",
        "limit": "all",
        "async": true
    }
    """
    data = request.get_json() or {}

    inventory = data.get('inventory', 'hosts')
    limit = data.get('limit')
    run_async = data.get('async', True)  # Default async for backups

    runner = AnsibleRunner(
        playbook='backup_configs.yml',
        inventory=inventory,
        limit=limit
    )

    if run_async:
        job_id = runner.run_async()
        return jsonify({
            'job_id': job_id,
            'status': 'running',
            'message': 'Configuration backup started in background',
            'check_status': f'/api/jobs/{job_id}'
        }), 202
    else:
        result = runner.run()
        return jsonify(result), 200 if result['return_code'] == 0 else 500


@app.route('/api/health/check', methods=['POST'])
def health_check():
    """
    Run network health check

    Request Body:
    {
        "inventory": "hosts",
        "limit": "all",
        "async": false
    }
    """
    data = request.get_json() or {}

    inventory = data.get('inventory', 'hosts')
    limit = data.get('limit')
    run_async = data.get('async', False)

    runner = AnsibleRunner(
        playbook='health_check.yml',
        inventory=inventory,
        limit=limit
    )

    if run_async:
        job_id = runner.run_async()
        return jsonify({
            'job_id': job_id,
            'status': 'running',
            'message': 'Health check started in background',
            'check_status': f'/api/jobs/{job_id}'
        }), 202
    else:
        result = runner.run()
        return jsonify(result), 200 if result['return_code'] == 0 else 500


@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """
    Get status of a job

    Response:
    {
        "id": "uuid",
        "status": "running|completed|failed|error",
        "playbook": "configure_vlans.yml",
        "started_at": "2024-01-01T10:00:00",
        "completed_at": "2024-01-01T10:05:00",
        "return_code": 0,
        "output": "...",
        "error": "..."
    }
    """
    if job_id not in jobs:
        return jsonify({
            'error': 'Job not found',
            'job_id': job_id
        }), 404

    return jsonify(jobs[job_id])


@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        'jobs': list(jobs.values()),
        'count': len(jobs)
    })


@app.route('/api/custom', methods=['POST'])
def run_custom_playbook():
    """
    Run any custom playbook

    Request Body:
    {
        "playbook": "configure_vlans.yml",
        "inventory": "hosts",
        "extra_vars": {"key": "value"},
        "tags": "vlans,interfaces",
        "limit": "switch1",
        "async": true
    }
    """
    data = request.get_json()

    if not data or 'playbook' not in data:
        return jsonify({
            'error': 'Playbook name is required',
            'example': {
                'playbook': 'configure_vlans.yml',
                'inventory': 'hosts',
                'async': True
            }
        }), 400

    playbook = data['playbook']
    inventory = data.get('inventory', 'hosts')
    extra_vars = data.get('extra_vars')
    tags = data.get('tags')
    limit = data.get('limit')
    run_async = data.get('async', False)

    # Validate playbook exists
    playbook_path = PLAYBOOKS_DIR / playbook
    if not playbook_path.exists():
        return jsonify({
            'error': f'Playbook not found: {playbook}',
            'available': [f.name for f in PLAYBOOKS_DIR.glob('*.yml')]
        }), 404

    runner = AnsibleRunner(
        playbook=playbook,
        inventory=inventory,
        extra_vars=extra_vars,
        tags=tags,
        limit=limit
    )

    if run_async:
        job_id = runner.run_async()
        return jsonify({
            'job_id': job_id,
            'status': 'running',
            'message': f'Playbook {playbook} started in background',
            'check_status': f'/api/jobs/{job_id}'
        }), 202
    else:
        result = runner.run()
        return jsonify(result), 200 if result['return_code'] == 0 else 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print(" "*20 + "ANSIBLE AUTOMATION API")
    print("="*70)
    print(f"\nPlaybooks directory: {PLAYBOOKS_DIR}")
    print(f"Inventory directory: {INVENTORY_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    print(f"\nAPI Server starting on http://0.0.0.0:5000")
    print("\nAvailable endpoints:")
    print("  POST http://localhost:5000/api/vlans/configure")
    print("  POST http://localhost:5000/api/ospf/configure")
    print("  POST http://localhost:5000/api/backup/configs")
    print("  POST http://localhost:5000/api/health/check")
    print("  GET  http://localhost:5000/api/playbooks")
    print("  GET  http://localhost:5000/api/jobs/<job_id>")
    print("\n" + "="*70)

    app.run(host='0.0.0.0', port=5000, debug=True)
