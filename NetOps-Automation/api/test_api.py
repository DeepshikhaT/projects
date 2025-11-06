#!/usr/bin/env python3
"""
Test script for Ansible Automation API
=======================================
Simple script to test all API endpoints

Usage:
    python test_api.py
"""

import requests
import time

API_URL = "http://localhost:5000"

def test_api():
    """Test all API endpoints"""

    print("="*70)
    print(" "*20 + "API TESTING")
    print("="*70)

    # Test 1: Check API is running
    print("\n[TEST 1] Checking API availability...")
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            print("✓ API is running")
            print(f"  Response: {response.json()['message']}")
        else:
            print("✗ API returned unexpected status")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API. Is it running?")
        print("  Start with: python ansible_api.py")
        return False

    # Test 2: List playbooks
    print("\n[TEST 2] Listing available playbooks...")
    response = requests.get(f"{API_URL}/api/playbooks")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['count']} playbooks")
        for pb in data['playbooks']:
            print(f"  - {pb['name']}")
    else:
        print("✗ Failed to list playbooks")

    # Test 3: List jobs
    print("\n[TEST 3] Listing jobs...")
    response = requests.get(f"{API_URL}/api/jobs")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Current jobs: {data['count']}")
    else:
        print("✗ Failed to list jobs")

    # Test 4: Run VLAN configuration (async)
    print("\n[TEST 4] Triggering VLAN configuration (async)...")
    response = requests.post(
        f"{API_URL}/api/vlans/configure",
        json={"async": True, "limit": "access-sw-01"}
    )

    if response.status_code == 202:
        job_id = response.json()['job_id']
        print(f"✓ Job started: {job_id}")

        # Poll for completion
        print("  Polling for completion...")
        for i in range(12):  # 60 seconds max
            time.sleep(5)
            status_response = requests.get(f"{API_URL}/api/jobs/{job_id}")
            status = status_response.json()['status']
            print(f"    {i*5}s: {status}")

            if status in ['completed', 'failed', 'error', 'timeout']:
                if status == 'completed':
                    print(f"✓ Job completed successfully")
                else:
                    print(f"✗ Job {status}")
                break
    else:
        print("✗ Failed to start job")

    print("\n" + "="*70)
    print(" "*25 + "TESTS COMPLETED")
    print("="*70)

if __name__ == '__main__':
    test_api()
