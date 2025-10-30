import requests
import random
import time
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

def create_sample_deployment(name, num_subdeployments=2, num_mhosts_per_sub=3):
    print(f"\n{'='*60}")
    print(f"Creating deployment: {name}")
    print(f"{'='*60}")

    deployment_response = requests.post(f'{BASE_URL}/deployments', json={
        'name': name,
        'status': 'active'
    })

    if deployment_response.status_code != 201:
        print(f"Failed to create deployment: {deployment_response.json()}")
        return

    deployment = deployment_response.json()
    print(f"✓ Created deployment: {deployment['name']} (ID: {deployment['id']})")

    for i in range(num_subdeployments):
        subdep_name = f"{name}-sub-{i+1}"
        subdep_response = requests.post(f'{BASE_URL}/subdeployments', json={
            'name': subdep_name,
            'deployment_id': deployment['id'],
            'status': 'active'
        })

        if subdep_response.status_code != 201:
            print(f"Failed to create subdeployment: {subdep_response.json()}")
            continue

        subdeployment = subdep_response.json()
        print(f"  ✓ Created subdeployment: {subdeployment['name']} (ID: {subdeployment['id']})")

        for j in range(num_mhosts_per_sub):
            hostname = f"host-{name.lower()}-{i+1}-{j+1}.example.com"
            status = random.choice(['online', 'offline', 'maintenance'])

            config = {
                'ip': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'port': random.choice([22, 80, 443, 8080]),
                'os': random.choice(['Ubuntu 22.04', 'CentOS 8', 'Debian 11']),
                'cpu_cores': random.choice([2, 4, 8, 16]),
                'memory_gb': random.choice([4, 8, 16, 32])
            }

            mhost_response = requests.post(f'{BASE_URL}/mhosts', json={
                'hostname': hostname,
                'subdeployment_id': subdeployment['id'],
                'status': status,
                'config': str(config)
            })

            if mhost_response.status_code == 201:
                print(f"    ✓ Created mhost: {hostname} (Status: {status})")
            else:
                print(f"    ✗ Failed to create mhost: {hostname}")

def simulate_monitoring():
    print(f"\n{'='*60}")
    print("Starting monitoring simulation...")
    print(f"{'='*60}\n")

    while True:
        try:
            mhosts_response = requests.get(f'{BASE_URL}/mhosts')
            if mhosts_response.status_code == 200:
                mhosts = mhosts_response.json()

                for mhost in mhosts:
                    new_status = random.choice(['online', 'offline', 'maintenance'])

                    if mhost['status'] != new_status:
                        update_response = requests.put(
                            f"{BASE_URL}/mhosts/{mhost['id']}",
                            json={'status': new_status}
                        )

                        if update_response.status_code == 200:
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"[{timestamp}] Updated {mhost['hostname']}: {mhost['status']} → {new_status}")

            time.sleep(5)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error during monitoring: {e}")
            time.sleep(5)

def display_stats():
    print(f"\n{'='*60}")
    print("System Statistics")
    print(f"{'='*60}")

    try:
        stats_response = requests.get(f'{BASE_URL}/stats')
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"Total Deployments:      {stats['total_deployments']}")
            print(f"Total Subdeployments:   {stats['total_subdeployments']}")
            print(f"Total Mhosts:           {stats['total_mhosts']}")
            print(f"Active Mhosts:          {stats['active_mhosts']}")
            print(f"Offline Mhosts:         {stats['offline_mhosts']}")
        else:
            print("Failed to fetch stats")
    except Exception as e:
        print(f"Error fetching stats: {e}")

    print(f"{'='*60}\n")

def display_audit_logs(limit=10):
    print(f"\n{'='*60}")
    print(f"Recent Audit Logs (Last {limit})")
    print(f"{'='*60}")

    try:
        audit_response = requests.get(f'{BASE_URL}/audit?limit={limit}')
        if audit_response.status_code == 200:
            logs = audit_response.json()
            for log in logs:
                print(f"[{log['timestamp']}] {log['entity_type']} #{log['entity_id']} - {log['action']}")
                if log['details']:
                    print(f"  └─ {log['details']}")
        else:
            print("Failed to fetch audit logs")
    except Exception as e:
        print(f"Error fetching audit logs: {e}")

    print(f"{'='*60}\n")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python automation.py setup       - Create sample data")
        print("  python automation.py monitor     - Start monitoring simulation")
        print("  python automation.py stats       - Display system statistics")
        print("  python automation.py audit       - Display audit logs")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'setup':
        create_sample_deployment('Production', num_subdeployments=3, num_mhosts_per_sub=5)
        create_sample_deployment('Staging', num_subdeployments=2, num_mhosts_per_sub=3)
        create_sample_deployment('Development', num_subdeployments=1, num_mhosts_per_sub=2)
        print("\n✓ Sample data created successfully!")
        display_stats()
    elif command == 'monitor':
        simulate_monitoring()
    elif command == 'stats':
        display_stats()
    elif command == 'audit':
        display_audit_logs(limit=20)
    else:
        print(f"Unknown command: {command}")
