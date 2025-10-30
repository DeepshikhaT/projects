# NetOps-Automation: Enterprise Network Automation with Ansible

## 🌐 Project Overview

NetOps-Automation is a comprehensive network automation project demonstrating real-world network engineering skills using Ansible. This project automates configuration, monitoring, and management of enterprise network infrastructure including routers, switches, and firewalls.

## 🎯 What This Project Demonstrates

This project showcases the skills that network engineers use daily in production environments:

- **Network Device Configuration:** Automated setup of routers and switches
- **Routing Protocols:** OSPF, BGP configuration and management
- **VLAN Management:** Creating, configuring, and monitoring VLANs
- **Configuration Backup:** Automated backup and restore procedures
- **Network Monitoring:** Health checks and performance monitoring
- **Compliance Checking:** Network security and configuration validation
- **Documentation:** Auto-generated network documentation

## 🛠️ Technology Stack

### Core Technologies
- **Ansible 2.15+**: Network automation and orchestration
- **Python 3.8+**: Custom scripts and monitoring tools
- **Jinja2**: Configuration templating
- **YAML**: Playbook and inventory definition
- **Netmiko**: Python library for network device connections
- **Paramiko**: SSH connectivity

### Network Protocols Covered
- **Layer 2:** VLANs, STP, VTP, Port Security
- **Layer 3:** OSPF, BGP, Static Routing
- **Management:** SNMP, Syslog, NTP
- **Security:** ACLs, Port Security, SSH

### Supported Vendors
- Cisco IOS/IOS-XE
- Cisco NX-OS
- Juniper Junos (concepts)
- Arista EOS (concepts)

## 📁 Project Structure

```
NetOps-Automation/
│
├── ansible.cfg                 # Ansible configuration
├── inventory/
│   ├── production/
│   │   ├── hosts              # Production inventory
│   │   └── group_vars/        # Group-specific variables
│   └── lab/
│       ├── hosts              # Lab/testing inventory
│       └── group_vars/
│
├── playbooks/
│   ├── configure_vlans.yml    # VLAN configuration
│   ├── configure_ospf.yml     # OSPF routing setup
│   ├── configure_bgp.yml      # BGP configuration
│   ├── backup_configs.yml     # Configuration backup
│   ├── restore_configs.yml    # Configuration restore
│   ├── interface_config.yml   # Interface management
│   ├── gather_facts.yml       # Device information gathering
│   ├── health_check.yml       # Network health monitoring
│   └── compliance_check.yml   # Security compliance
│
├── roles/
│   ├── common/                # Common network tasks
│   ├── vlan_config/          # VLAN configuration role
│   ├── routing/              # Routing protocol role
│   ├── monitoring/           # Monitoring role
│   └── backup/               # Backup role
│
├── templates/
│   ├── cisco_ios/
│   │   ├── vlan.j2           # VLAN template
│   │   ├── ospf.j2           # OSPF template
│   │   └── interface.j2      # Interface template
│   └── reports/
│       └── network_report.j2  # Documentation template
│
├── scripts/
│   ├── network_monitor.py     # Real-time monitoring
│   ├── config_differ.py       # Configuration comparison
│   ├── topology_mapper.py     # Network topology visualization
│   └── compliance_scanner.py  # Compliance checking
│
├── configs/
│   ├── backups/              # Configuration backups
│   └── golden/               # Golden configuration templates
│
├── vars/
│   ├── vlans.yml             # VLAN definitions
│   ├── routing.yml           # Routing configurations
│   └── interfaces.yml        # Interface configurations
│
├── docs/
│   ├── NETWORK_TOPOLOGY.md   # Network diagrams
│   ├── PLAYBOOK_GUIDE.md     # How to use playbooks
│   └── PROTOCOLS.md          # Protocol documentation
│
├── tests/
│   └── test_playbooks.py     # Playbook testing
│
└── requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

1. **Install Ansible:**
   ```bash
   pip install ansible
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure network access:**
   - Ensure SSH access to network devices
   - Have appropriate credentials

### Basic Usage

#### 1. Configure VLANs
```bash
ansible-playbook playbooks/configure_vlans.yml -i inventory/lab/hosts
```

#### 2. Setup OSPF Routing
```bash
ansible-playbook playbooks/configure_ospf.yml -i inventory/lab/hosts
```

#### 3. Backup All Configurations
```bash
ansible-playbook playbooks/backup_configs.yml -i inventory/production/hosts
```

#### 4. Run Health Check
```bash
ansible-playbook playbooks/health_check.yml -i inventory/production/hosts
```

#### 5. Generate Network Documentation
```bash
python scripts/topology_mapper.py --inventory inventory/production/hosts
```

## 📋 Real-World Use Cases

### Use Case 1: Deploy New VLANs Across Campus
**Scenario:** Need to add VLAN 100 (Guest WiFi) to 50 switches

**Traditional Way:**
- Manually SSH to each switch
- Type commands 50 times
- Risk of typos and inconsistencies
- Takes hours

**With This Automation:**
```bash
# Edit vars/vlans.yml to add VLAN 100
# Run one command:
ansible-playbook playbooks/configure_vlans.yml -i inventory/production/hosts
# Done in minutes, consistent across all devices
```

### Use Case 2: Disaster Recovery
**Scenario:** Router configuration corrupted, need immediate restore

**With This Automation:**
```bash
ansible-playbook playbooks/restore_configs.yml -i inventory/production/hosts --limit core-router-01
# Restores last known good configuration in seconds
```

### Use Case 3: Daily Health Monitoring
**Scenario:** Check all devices for issues every morning

**With This Automation:**
```bash
ansible-playbook playbooks/health_check.yml -i inventory/production/hosts
# Generates report of:
# - Interface status
# - CPU/Memory usage
# - Routing protocol status
# - Configuration drift
```

## 🔧 Example Playbooks Explained

### VLAN Configuration Playbook

**What it does:** Creates and configures VLANs across multiple switches

```yaml
# playbooks/configure_vlans.yml
---
- name: Configure VLANs on switches
  hosts: switches
  gather_facts: no

  tasks:
    - name: Load VLAN definitions
      include_vars: ../vars/vlans.yml

    - name: Create VLANs
      cisco.ios.ios_vlans:
        config:
          - vlan_id: "{{ item.id }}"
            name: "{{ item.name }}"
            state: active
        state: merged
      loop: "{{ vlans }}"

    - name: Assign VLANs to interfaces
      cisco.ios.ios_l2_interfaces:
        config:
          - name: "{{ item.interface }}"
            mode: access
            access:
              vlan: "{{ item.vlan_id }}"
        state: merged
      loop: "{{ vlan_assignments }}"
```

### OSPF Configuration Playbook

**What it does:** Configures OSPF routing protocol on routers

```yaml
# playbooks/configure_ospf.yml
---
- name: Configure OSPF on routers
  hosts: routers
  gather_facts: no

  tasks:
    - name: Configure OSPF process
      cisco.ios.ios_ospf:
        config:
          processes:
            - process_id: 1
              router_id: "{{ ospf_router_id }}"
              areas:
                - area_id: "0.0.0.0"
                  networks:
                    - address: "{{ item.network }}"
                      wildcard: "{{ item.wildcard }}"
              loop: "{{ ospf_networks }}"
        state: merged
```

### Network Health Check Playbook

**What it does:** Monitors device health and generates report

```yaml
# playbooks/health_check.yml
---
- name: Network Health Check
  hosts: all
  gather_facts: yes

  tasks:
    - name: Check interface status
      cisco.ios.ios_command:
        commands:
          - show ip interface brief
      register: interface_status

    - name: Check CPU usage
      cisco.ios.ios_command:
        commands:
          - show processes cpu | include CPU
      register: cpu_usage

    - name: Check memory usage
      cisco.ios.ios_command:
        commands:
          - show memory statistics
      register: memory_usage

    - name: Generate health report
      template:
        src: ../templates/reports/health_report.j2
        dest: ../reports/health_{{ inventory_hostname }}_{{ ansible_date_time.date }}.txt
```

## 🐍 Python Scripts

### Network Monitoring Script

**Purpose:** Real-time monitoring of network devices

```python
# scripts/network_monitor.py
import netmiko
import time
import json

def monitor_device(device_info):
    """Monitor a single network device"""
    connection = netmiko.ConnectHandler(**device_info)

    # Check interface status
    interfaces = connection.send_command('show ip interface brief', use_textfsm=True)

    # Check routing table
    routes = connection.send_command('show ip route summary', use_textfsm=True)

    # Check CPU and memory
    cpu = connection.send_command('show processes cpu | include CPU')
    memory = connection.send_command('show memory statistics')

    return {
        'interfaces': interfaces,
        'routes': routes,
        'cpu': cpu,
        'memory': memory
    }
```

### Configuration Backup Script

**Purpose:** Automated configuration backups with version control

```python
# scripts/backup_runner.py
import os
from datetime import datetime
from netmiko import ConnectHandler

def backup_device_config(device):
    """Backup configuration from network device"""
    connection = ConnectHandler(**device)
    config = connection.send_command('show running-config')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"backups/{device['host']}_{timestamp}.cfg"

    with open(filename, 'w') as f:
        f.write(config)

    return filename
```

## 📊 Network Monitoring Dashboard

The project includes a Python script that generates a real-time dashboard:

```bash
python scripts/network_monitor.py --inventory inventory/production/hosts
```

**Dashboard shows:**
- Device reachability (ping status)
- Interface up/down status
- CPU and memory utilization
- Routing protocol status
- Configuration drift detection

## 🔐 Security Best Practices

### Credential Management

**Never hardcode credentials!** This project uses Ansible Vault:

```bash
# Create encrypted credential file
ansible-vault create inventory/production/group_vars/all/vault.yml

# Add credentials:
vault_ssh_user: admin
vault_ssh_password: SecurePassword123
vault_enable_password: EnablePass456
```

### SSH Key Authentication

```bash
# Generate SSH keys for network devices
ssh-keygen -t rsa -b 4096 -f ~/.ssh/network_automation

# Copy to devices (if supported)
ssh-copy-id -i ~/.ssh/network_automation.pub admin@router1
```

## 🧪 Testing

### Test Playbooks Before Production

```bash
# Syntax check
ansible-playbook playbooks/configure_vlans.yml --syntax-check

# Dry run (check mode)
ansible-playbook playbooks/configure_vlans.yml --check

# Test on lab environment first
ansible-playbook playbooks/configure_vlans.yml -i inventory/lab/hosts
```

### Python Script Testing

```bash
python -m pytest tests/
```

## 📈 Skills Demonstrated

### Network Engineering Skills
- ✅ Layer 2 switching (VLANs, STP, trunking)
- ✅ Layer 3 routing (OSPF, BGP, static routes)
- ✅ Network design and topology
- ✅ Configuration management
- ✅ Troubleshooting methodology
- ✅ Network security (ACLs, port security)
- ✅ Network monitoring and management

### Automation Skills
- ✅ Ansible playbook development
- ✅ Jinja2 templating
- ✅ YAML configuration
- ✅ Python scripting for networks
- ✅ Version control (Git)
- ✅ Infrastructure as Code (IaC)
- ✅ CI/CD for network configs

### DevOps/NetDevOps Skills
- ✅ Automation mindset
- ✅ Idempotent operations
- ✅ Configuration as code
- ✅ Testing and validation
- ✅ Documentation
- ✅ Error handling
- ✅ Logging and monitoring

## 🎓 Learning Resources

### Protocols Covered

**OSPF (Open Shortest Path First):**
- Link-state routing protocol
- Area-based design
- Configures shortest path first algorithm
- Use case: Enterprise campus networks

**BGP (Border Gateway Protocol):**
- Path vector protocol
- Used for internet routing
- AS (Autonomous System) based
- Use case: ISP networks, multi-homing

**VLANs (Virtual LANs):**
- Layer 2 segmentation
- Broadcast domain separation
- Security and performance benefits
- Use case: Department/function separation

## 🔄 Common Network Tasks Automated

### 1. Initial Device Setup
```bash
ansible-playbook playbooks/initial_setup.yml -i inventory/lab/hosts
```
Configures:
- Hostname
- Management IP
- SSH access
- NTP
- Syslog
- SNMP

### 2. Interface Configuration
```bash
ansible-playbook playbooks/interface_config.yml -i inventory/production/hosts --tags "uplinks"
```
Configures:
- IP addresses
- Descriptions
- Speed/duplex
- Port security

### 3. Routing Protocol Deployment
```bash
ansible-playbook playbooks/configure_ospf.yml -i inventory/production/hosts
```
Configures:
- Router ID
- Network statements
- Area assignments
- Authentication

### 4. VLAN Provisioning
```bash
ansible-playbook playbooks/configure_vlans.yml -i inventory/production/hosts
```
Creates and assigns:
- VLAN database entries
- Access port assignments
- Trunk port configurations
- Inter-VLAN routing

## 📊 Compliance and Auditing

### Configuration Compliance Check
```bash
ansible-playbook playbooks/compliance_check.yml -i inventory/production/hosts
```

**Checks for:**
- ✅ SSH enabled, Telnet disabled
- ✅ Strong password policies
- ✅ NTP configured
- ✅ Syslog configured
- ✅ SNMP v3 (not v1/v2)
- ✅ No default passwords
- ✅ ACLs on management interfaces

### Configuration Drift Detection
```bash
python scripts/config_differ.py --device router1 --baseline configs/golden/router1.cfg
```

Shows differences between current and baseline configurations.

## 🚀 Deployment Workflow

### Recommended Workflow

```
1. Development
   ├── Create playbook in dev environment
   ├── Test on GNS3/EVE-NG lab
   └── Peer review

2. Testing
   ├── Run syntax check
   ├── Run in check mode
   ├── Test on lab inventory
   └── Validate results

3. Staging
   ├── Deploy to staging environment
   ├── Run health checks
   ├── Verify no issues
   └── Get approval

4. Production
   ├── Schedule maintenance window
   ├── Backup current configs
   ├── Deploy playbook
   ├── Verify and validate
   └── Document changes
```

## 🎯 Real Interview Questions This Project Helps Answer

**Q: "How do you manage configuration across 100+ network devices?"**
A: "I use Ansible for centralized configuration management. I define configurations in YAML, use Jinja2 templates for device-specific settings, and deploy via playbooks. This ensures consistency and reduces human error."

**Q: "Describe your backup and disaster recovery strategy."**
A: "I have automated daily configuration backups using Ansible. Backups are version-controlled and stored with timestamps. For DR, I have tested restore playbooks that can rebuild device configs in minutes."

**Q: "How do you ensure network security compliance?"**
A: "I use compliance checking playbooks that verify security baselines: SSH only (no Telnet), strong passwords, ACLs, SNMP v3, and NTP. Any non-compliant devices are flagged in reports."

**Q: "How do you handle network changes safely?"**
A: "I follow a strict workflow: test in lab first, use Ansible check mode, deploy to staging, then production during maintenance windows. All changes are version-controlled and reversible."

## 📚 Additional Documentation

- **[NETWORK_TOPOLOGY.md](docs/NETWORK_TOPOLOGY.md)** - Network diagrams and design
- **[PLAYBOOK_GUIDE.md](docs/PLAYBOOK_GUIDE.md)** - Detailed playbook usage
- **[PROTOCOLS.md](docs/PROTOCOLS.md)** - Protocol configuration details
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🔮 Future Enhancements

- [ ] Terraform integration for cloud networking
- [ ] Webhook integration for ChatOps
- [ ] Automated testing with pyATS/Genie
- [ ] Integration with monitoring tools (Nagios, Zabbix)
- [ ] Network CI/CD pipeline
- [ ] Intent-based networking concepts
- [ ] SD-WAN automation

## 👤 Author

**Deepshikha Tripathi**

This project demonstrates:
- Network engineering expertise
- Automation and scripting skills
- Infrastructure as Code practices
- Real-world problem-solving
- Industry best practices

## 📄 License

This is a portfolio/demonstration project.

## 🤝 Contributing

This is a personal portfolio project, but feedback and suggestions are welcome!

---

**Note:** This project uses simulated network environments for demonstration. Adapt configurations for your specific network equipment and requirements.
