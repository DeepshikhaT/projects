# Ansible Automation API

REST API to trigger Ansible playbooks programmatically.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

### 2. Start API Server

```bash
cd NetOps-Automation/api
python ansible_api.py
```

Server starts on: `http://localhost:5000`

### 3. Test API

```bash
# List available playbooks
curl http://localhost:5000/api/playbooks

# Configure VLANs
curl -X POST http://localhost:5000/api/vlans/configure \
  -H "Content-Type: application/json" \
  -d '{"async": true}'
```

---

## 📖 API Documentation

### List Available Playbooks

**GET** `/api/playbooks`

**Response:**
```json
{
  "playbooks": [
    {
      "name": "configure_vlans.yml",
      "path": "playbooks/configure_vlans.yml",
      "size": 2048,
      "modified": "2024-01-01T10:00:00"
    }
  ],
  "count": 1
}
```

---

### Configure VLANs

**POST** `/api/vlans/configure`

**Request Body:**
```json
{
  "inventory": "hosts",
  "limit": "switch1,switch2",
  "async": true
}
```

**Response (Async):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "message": "VLAN configuration started in background",
  "check_status": "/api/jobs/550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (Sync):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "playbook": "configure_vlans.yml",
  "started_at": "2024-01-01T10:00:00",
  "completed_at": "2024-01-01T10:05:00",
  "return_code": 0,
  "output": "... ansible output ...",
  "error": ""
}
```

---

### Configure OSPF

**POST** `/api/ospf/configure`

**Request Body:**
```json
{
  "inventory": "hosts",
  "limit": "router1,router2",
  "async": false
}
```

---

### Backup Configurations

**POST** `/api/backup/configs`

**Request Body:**
```json
{
  "inventory": "hosts",
  "limit": "all",
  "async": true
}
```

---

### Health Check

**POST** `/api/health/check`

**Request Body:**
```json
{
  "inventory": "hosts",
  "async": false
}
```

---

### Get Job Status

**GET** `/api/jobs/<job_id>`

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "playbook": "configure_vlans.yml",
  "started_at": "2024-01-01T10:00:00",
  "completed_at": "2024-01-01T10:05:00",
  "return_code": 0,
  "output": "PLAY [Configure VLANs]...",
  "error": ""
}
```

---

### List All Jobs

**GET** `/api/jobs`

**Response:**
```json
{
  "jobs": [
    {
      "id": "job-uuid-1",
      "status": "completed",
      "playbook": "configure_vlans.yml"
    },
    {
      "id": "job-uuid-2",
      "status": "running",
      "playbook": "backup_configs.yml"
    }
  ],
  "count": 2
}
```

---

### Run Custom Playbook

**POST** `/api/custom`

**Request Body:**
```json
{
  "playbook": "configure_vlans.yml",
  "inventory": "hosts",
  "extra_vars": {"vlan_id": 100},
  "tags": "vlans",
  "limit": "switch1",
  "async": true
}
```

---

## 🐍 Python Client Example

```python
import requests
import time

API_URL = "http://localhost:5000"

# 1. Configure VLANs (async)
response = requests.post(
    f"{API_URL}/api/vlans/configure",
    json={"async": True, "limit": "switch1"}
)

job_id = response.json()['job_id']
print(f"Job started: {job_id}")

# 2. Poll for completion
while True:
    status = requests.get(f"{API_URL}/api/jobs/{job_id}").json()
    print(f"Status: {status['status']}")

    if status['status'] in ['completed', 'failed', 'error']:
        print(f"Final status: {status['status']}")
        print(f"Output: {status['output']}")
        break

    time.sleep(5)

# 3. Run health check (sync)
response = requests.post(
    f"{API_URL}/api/health/check",
    json={"async": False}
)

if response.status_code == 200:
    print("Health check passed!")
    print(response.json()['output'])
```

---

## 🔧 Integration with CI/CD

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Deploy Network Config') {
            steps {
                script {
                    // Trigger VLAN configuration
                    def response = httpRequest(
                        url: 'http://ansible-api:5000/api/vlans/configure',
                        httpMode: 'POST',
                        contentType: 'APPLICATION_JSON',
                        requestBody: '{"async": false, "inventory": "production"}'
                    )

                    if (response.status != 200) {
                        error "VLAN configuration failed"
                    }
                }
            }
        }
    }
}
```

### GitLab CI

```yaml
deploy_network:
  script:
    - |
      curl -X POST http://ansible-api:5000/api/vlans/configure \
        -H "Content-Type: application/json" \
        -d '{"async": false, "inventory": "production"}'
  only:
    - main
```

---

## 🐳 Docker Deployment

```yaml
# docker-compose.yml
version: '3'
services:
  ansible-api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ../playbooks:/app/playbooks
      - ../inventory:/app/inventory
    environment:
      - FLASK_ENV=production
```

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ansible openssh-client

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ansible_api.py .

CMD ["python", "ansible_api.py"]
```

---

## 🔐 Production Considerations

### 1. Authentication

```python
from functools import wraps
from flask import request

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'your-secret-key':
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/vlans/configure', methods=['POST'])
@require_api_key
def configure_vlans():
    # ... your code ...
```

### 2. Job Storage (Use Redis)

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Store job
r.setex(job_id, 3600, json.dumps(job_data))  # Expire after 1 hour

# Retrieve job
job_data = json.loads(r.get(job_id))
```

### 3. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/api/vlans/configure', methods=['POST'])
@limiter.limit("10 per minute")
def configure_vlans():
    # ... your code ...
```

---

## 🎯 Use Cases

### 1. CI/CD Pipeline Integration
- Trigger network configurations on code deploy
- Automated testing of network changes
- Rollback on failure

### 2. Self-Service Portal
- Allow developers to configure VLANs
- Network team approves via API
- Audit trail maintained

### 3. Scheduled Automation
- Nightly configuration backups
- Regular health checks
- Automated compliance checks

### 4. Event-Driven Automation
- Webhook triggers playbook
- Auto-remediation on alerts
- Dynamic scaling

---

## 📝 Logging

Logs are stored in: `logs/api/`

Each job creates a log file: `logs/api/<job_id>.log`

**Log Contents:**
```
Command: ansible-playbook playbooks/configure_vlans.yml -i inventory/lab/hosts -v
Return Code: 0

STDOUT:
PLAY [Configure VLANs on Switches] *********************************************
TASK [Create VLANs] ************************************************************
changed: [switch1]
...

STDERR:
(any errors)
```

---

## 🧪 Testing

```bash
# Test with curl
bash test_api.sh

# Test with Python
python test_api.py

# Test with Postman
# Import: postman_collection.json
```

---

## 🐛 Troubleshooting

### API won't start
```bash
# Check if port 5000 is already in use
netstat -ano | findstr :5000

# Kill process if needed (Windows)
taskkill /PID <pid> /F
```

### Playbook fails
```bash
# Check logs
cat logs/api/<job_id>.log

# Test playbook manually
ansible-playbook playbooks/configure_vlans.yml -i inventory/lab/hosts
```

### Job not found
- Jobs are stored in memory (lost on restart)
- Implement Redis for persistent storage

---

## 💡 Tips

1. **Use async for long-running playbooks** (backup, large deployments)
2. **Use sync for quick operations** (health checks, single device)
3. **Limit operations** during testing (`"limit": "test-device"`)
4. **Check job status** before assuming completion
5. **Implement authentication** in production

---

## 🎓 Learning More

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ansible API](https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html)
- [REST API Best Practices](https://restfulapi.net/)

---

**Created by:** Deepshikha Tripathi
**Purpose:** Enable API-driven network automation
