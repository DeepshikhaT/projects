# NetOps-Automation - Complete Interview Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Network Engineering Fundamentals](#network-engineering-fundamentals)
3. [Ansible Deep Dive](#ansible-deep-dive)
4. [Network Protocols Explained](#network-protocols-explained)
5. [Python for Network Automation](#python-for-network-automation)
6. [Common Interview Questions](#common-interview-questions)
7. [Live Demo Scenarios](#live-demo-scenarios)
8. [Troubleshooting Scenarios](#troubleshooting-scenarios)
9. [How to Present This Project](#how-to-present-this-project)

---

## Project Overview

### What is NetOps-Automation?

**Simple Explanation:**
"NetOps-Automation is a network automation project I built using Ansible and Python to automate the configuration, monitoring, and management of enterprise network infrastructure. Instead of manually configuring routers and switches one by one, I use automation to deploy consistent configurations across hundreds of devices in minutes."

**Business Value:**
- **Time Savings:** Configure 100 switches in 5 minutes vs. 2-3 days manually
- **Consistency:** Eliminates human errors and configuration drift
- **Scalability:** Easy to scale from 10 to 1000 devices
- **Documentation:** Self-documenting through code
- **Disaster Recovery:** Quick restoration from backups
- **Compliance:** Automated security and compliance checking

**Why I Built It:**
"I wanted to demonstrate modern network engineering skills. Today's network engineers need to know both traditional networking (OSPF, VLANs, routing) AND automation tools (Ansible, Python). This project shows I can do both."

---

## Network Engineering Fundamentals

### OSI Model (Must Know!)

```
7. Application    - HTTP, FTP, SMTP (user applications)
6. Presentation   - SSL/TLS, data formatting
5. Session        - Session management
4. Transport      - TCP/UDP (port numbers)
3. Network        - IP addresses, routing (OSPF, BGP)
2. Data Link      - MAC addresses, switching (VLANs)
1. Physical       - Cables, signals
```

**Interview Tip:** When discussing any network issue, reference the OSI layer!

**Example:**
- "VLAN issue? That's Layer 2 - Data Link layer"
- "Routing problem? Layer 3 - Network layer"
- "Application not responding? Could be Layer 4 (ports) or Layer 7 (application)"

### TCP/IP Model (Practical Version)

```
4. Application    - Combines OSI 5-7
3. Transport      - TCP/UDP
2. Internet       - IP, ICMP, routing protocols
1. Network Access - Combines OSI 1-2
```

---

## Network Protocols Explained

### VLANs (Virtual LANs)

**What it is:**
"VLANs are a way to segment a physical network into multiple logical networks. Think of it like creating separate broadcast domains within the same physical infrastructure."

**Why we use VLANs:**
1. **Security:** Separate guest WiFi from corporate network
2. **Performance:** Reduce broadcast traffic
3. **Organization:** Group devices by department/function
4. **Flexibility:** Move users between VLANs without physical changes

**Example Configuration:**
```
! Create VLAN
vlan 10
 name DATA

! Assign port to VLAN
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
 description User Port - Finance Dept
```

**My Project Implementation:**
```yaml
# vars/vlans.yml
vlans:
  - id: 10
    name: Management
    description: Network Management VLAN
```

```yaml
# playbooks/configure_vlans.yml
- name: Create VLANs
  cisco.ios.ios_vlans:
    config:
      - vlan_id: "{{ item.id }}"
        name: "{{ item.name }}"
        state: active
    state: merged
  loop: "{{ vlans }}"
```

**Interview Questions:**

**Q: "What's the difference between access port and trunk port?"**
A: "Access port carries traffic for ONE VLAN - connects end devices like computers. Trunk port carries traffic for MULTIPLE VLANs - connects switches together. Trunk ports use 802.1Q tagging to identify which VLAN each frame belongs to."

**Q: "What's a native VLAN?"**
A: "On a trunk port, the native VLAN is the VLAN whose traffic is NOT tagged. By default it's VLAN 1, but best practice is to change it to an unused VLAN for security. Untagged traffic from the trunk is placed in the native VLAN."

**Q: "Why use VLANs instead of physical separation?"**
A: "Cost and flexibility. Instead of buying separate switches for each department, I can use VLANs to logically separate them on the same physical infrastructure. It's also easier to move users between VLANs without physically relocating them."

### OSPF (Open Shortest Path First)

**What it is:**
"OSPF is a link-state routing protocol. Routers share information about their directly connected links, and each router builds a complete map of the network. Then they use Dijkstra's algorithm (SPF - Shortest Path First) to calculate the best path to each destination."

**Key Concepts:**

1. **Areas:** OSPF divides network into areas for scalability
   - Area 0 = Backbone area (all other areas must connect to it)
   - Area 1, 2, 3... = Regular areas

2. **Router ID:** Unique identifier for each router
   - Usually highest loopback IP or highest interface IP
   - Can be manually configured

3. **Neighbor States:**
   - Down → Init → 2-Way → ExStart → Exchange → Loading → Full
   - Full = neighbors are synchronized

4. **LSA (Link State Advertisement):** OSPF messages containing routing information

**Example Configuration:**
```
! Manual configuration
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.255.255 area 0
 network 192.168.1.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/0
```

**My Project Implementation:**
```yaml
# playbooks/configure_ospf.yml
- name: Configure OSPF router process
  cisco.ios.ios_config:
    lines:
      - "router ospf 1"
      - "router-id {{ ospf_router_id }}"
      - "network {{ item.network }} {{ item.wildcard }} area {{ item.area }}"
    loop: "{{ ospf_networks }}"
```

**Interview Questions:**

**Q: "OSPF vs BGP - when do you use each?"**
A:
- "OSPF is for INTERNAL routing (within your organization - like campus or data center). It's fast to converge and works well for networks up to a few thousand routers.
- BGP is for EXTERNAL routing (between organizations - like ISPs and the Internet). It's designed for huge scale and policy-based routing. BGP is slower to converge but more stable."

**Q: "How does OSPF calculate the best path?"**
A: "OSPF uses cost as its metric. Cost = Reference Bandwidth / Interface Bandwidth. Default reference bandwidth is 100 Mbps, so:
- FastEthernet (100 Mbps) = cost 1
- GigabitEthernet (1000 Mbps) = cost 1 (needs adjustment!)
- 10GigE (10000 Mbps) = cost 1 (needs adjustment!)

Best practice: Set 'auto-cost reference-bandwidth 10000' for modern networks."

**Q: "What happens if OSPF neighbors don't form?"**
A: "I troubleshoot systematically:
1. Check physical connectivity (ping)
2. Verify same subnet on both sides
3. Check OSPF is enabled on interfaces
4. Verify same area number
5. Check authentication matches (if enabled)
6. Verify MTU matches
7. Check ACLs aren't blocking OSPF (protocol 89)"

### BGP (Border Gateway Protocol)

**What it is:**
"BGP is the routing protocol of the Internet. It's a path vector protocol that routes between Autonomous Systems (AS). Think of AS as different organizations or ISPs."

**Key Concepts:**

1. **AS Number:** Unique number identifying an organization
   - Private: 64512-65535
   - Public: Assigned by IANA

2. **iBGP vs eBGP:**
   - iBGP: BGP between routers in SAME AS
   - eBGP: BGP between routers in DIFFERENT AS

3. **BGP Attributes (Path Selection):**
   - Weight (Cisco-specific, higher better)
   - Local Preference (higher better)
   - AS Path (shorter better)
   - MED (lower better)

**Example:**
```
router bgp 65001
 neighbor 203.0.113.1 remote-as 65000    ! eBGP to ISP
 neighbor 2.2.2.2 remote-as 65001        ! iBGP to other router
 network 10.0.0.0 mask 255.0.0.0         ! Advertise network
```

**Interview Question:**

**Q: "Why is BGP slow to converge?"**
A: "BGP is designed for stability over speed. It uses:
- Hold timers (typically 180 seconds)
- Route dampening (suppresses flapping routes)
- Policy-based routing (complex decision process)

This is intentional - on the Internet, it's better to be stable than fast. A flapping route could affect millions of users."

### STP (Spanning Tree Protocol)

**What it is:**
"STP prevents Layer 2 loops in switched networks. It creates a loop-free topology by blocking redundant paths and activating them if the primary path fails."

**Why we need it:**
Without STP, broadcast storms would crash the network in seconds!

**Port States:**
1. **Blocking:** Receives BPDUs only, doesn't forward data
2. **Listening:** Processes BPDUs, doesn't learn MAC addresses
3. **Learning:** Learns MAC addresses, doesn't forward data
4. **Forwarding:** Normal operation, forwards data
5. **Disabled:** Administratively shut down

**Modern Alternatives:**
- RSTP (Rapid STP) - Faster convergence
- MSTP (Multiple STP) - Multiple VLANs per instance
- PVST+ (Cisco) - One STP instance per VLAN

---

## Ansible Deep Dive

### What is Ansible?

**Simple Definition:**
"Ansible is an automation tool that lets me manage hundreds of devices by writing simple YAML files called playbooks. It's agentless - no software to install on network devices, just uses SSH."

**Why Ansible for Networks:**
1. **Agentless:** Only needs SSH (network devices already have this)
2. **Idempotent:** Run same playbook multiple times, safe result
3. **YAML:** Easy to read and write
4. **Modular:** Reusable roles and playbooks
5. **Large Community:** Lots of pre-built modules

### Key Ansible Concepts

#### 1. Inventory

**What it is:** List of devices Ansible manages

```ini
# inventory/lab/hosts
[routers]
router1 ansible_host=192.168.1.1
router2 ansible_host=192.168.1.2

[switches]
switch1 ansible_host=192.168.1.11
switch2 ansible_host=192.168.1.12

[all:vars]
ansible_connection=network_cli
ansible_network_os=ios
ansible_user=admin
ansible_password=cisco
```

**Interview Tip:** Never hardcode passwords! Use Ansible Vault:
```bash
ansible-vault encrypt_string 'mypassword' --name 'ansible_password'
```

#### 2. Playbook

**What it is:** YAML file describing automation tasks

```yaml
---
- name: Configure VLANs             # Play name
  hosts: switches                   # Target devices
  gather_facts: no                  # Don't collect facts

  tasks:                           # List of tasks
    - name: Create VLAN 10         # Task name
      cisco.ios.ios_vlans:         # Module to use
        config:
          - vlan_id: 10
            name: DATA
        state: merged              # Idempotent merge
```

**Playbook Structure:**
```
Playbook
  └─ Play 1
      ├─ Task 1
      ├─ Task 2
      └─ Task 3
  └─ Play 2
      ├─ Task 1
      └─ Task 2
```

#### 3. Modules

**What it is:** Pre-built code that performs specific actions

**Network Modules I Use:**

```yaml
# Configuration modules
cisco.ios.ios_vlans          # Manage VLANs
cisco.ios.ios_interfaces     # Manage interfaces
cisco.ios.ios_l2_interfaces  # Layer 2 config
cisco.ios.ios_l3_interfaces  # Layer 3 config
cisco.ios.ios_config         # Generic config

# Information gathering
cisco.ios.ios_command        # Run show commands
cisco.ios.ios_facts          # Collect device facts

# Configuration management
cisco.ios.ios_config         # Backup/restore
```

#### 4. Variables

**Multiple Ways to Define:**

```yaml
# In playbook
vars:
  vlan_id: 10
  vlan_name: DATA

# In separate file
vars_files:
  - vars/vlans.yml

# In inventory
[switches:vars]
dns_server=8.8.8.8

# At runtime
ansible-playbook playbook.yml -e "vlan_id=20"
```

#### 5. Templates (Jinja2)

**What it is:** Dynamic configuration generation

```jinja2
{# templates/cisco_ios/vlan.j2 #}
{% for vlan in vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
{% endfor %}
```

**Use in playbook:**
```yaml
- name: Generate VLAN config
  template:
    src: vlan.j2
    dest: /tmp/vlan_config.txt
```

#### 6. Handlers

**What it is:** Tasks that run only when notified (triggered by changes)

```yaml
tasks:
  - name: Modify configuration
    cisco.ios.ios_config:
      lines:
        - ntp server 10.0.0.1
    notify: save config        # Trigger handler

handlers:
  - name: save config
    cisco.ios.ios_config:
      save_when: always
```

### Ansible Best Practices

1. **Use roles for organization:**
```
roles/
  ├── vlan_config/
  │   ├── tasks/main.yml
  │   ├── vars/main.yml
  │   └── templates/
  └── routing/
      ├── tasks/main.yml
      └── vars/main.yml
```

2. **Always use check mode first:**
```bash
ansible-playbook playbook.yml --check  # Dry run
```

3. **Limit scope when testing:**
```bash
ansible-playbook playbook.yml --limit router1  # Only one device
```

4. **Tag tasks for selective execution:**
```yaml
- name: Configure VLAN
  cisco.ios.ios_vlans:
    config:
      - vlan_id: 10
  tags: vlans

# Run only vlan tasks:
# ansible-playbook playbook.yml --tags vlans
```

### Interview Questions - Ansible

**Q: "What makes Ansible idempotent?"**
A: "Idempotent means I can run the same playbook multiple times and get the same result - it won't keep applying changes. For example, if I run a playbook to create VLAN 10, and VLAN 10 already exists, Ansible detects this and skips that task. This is safe for production - I can re-run playbooks without worry."

**Q: "Ansible vs other tools (Puppet, Chef, SaltStack)?"**
A:
- "**Ansible:** Agentless (SSH), push-based, YAML, great for networks
- **Puppet/Chef:** Agent-based, pull-based, better for servers
- **SaltStack:** Agent-based, push or pull, faster but more complex
- I chose Ansible for networks because devices already have SSH and can't run agents."

**Q: "How do you handle secrets in Ansible?"**
A: "Multiple approaches:
1. **Ansible Vault:** Encrypt sensitive files
   ```bash
   ansible-vault create secrets.yml
   ```
2. **Environment variables:** For CI/CD pipelines
3. **External secret managers:** HashiCorp Vault, AWS Secrets Manager
4. **Never commit secrets to Git!**"

**Q: "How do you test Ansible playbooks?"**
A:
```
1. Syntax check:     ansible-playbook playbook.yml --syntax-check
2. Dry run:          ansible-playbook playbook.yml --check
3. Test environment: Run on lab devices first
4. Limit scope:      ansible-playbook playbook.yml --limit test-device
5. Molecule:         Testing framework for Ansible (advanced)
```

---

## Python for Network Automation

### Why Python for Networks?

1. **Flexibility:** Can do things Ansible can't
2. **Custom Logic:** Complex conditionals and calculations
3. **API Integration:** REST APIs, databases, monitoring tools
4. **Data Processing:** Parse and analyze network data
5. **Rapid Development:** Quick scripts for one-off tasks

### Key Libraries

#### 1. Netmiko (SSH to Network Devices)

**What it is:** Simplified SSH library for network devices

```python
from netmiko import ConnectHandler

# Device connection details
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco',  # Enable password
}

# Connect and execute commands
connection = ConnectHandler(**device)
connection.enable()  # Enter enable mode

output = connection.send_command('show ip interface brief')
print(output)

# Configure device
config_commands = [
    'vlan 10',
    'name DATA'
]
output = connection.send_config_set(config_commands)

connection.disconnect()
```

**Interview Question:**

**Q: "Why use Netmiko instead of paramiko?"**
A: "Paramiko is a low-level SSH library - very flexible but requires handling device prompts, pagination, enable mode manually. Netmiko is built on paramiko but adds network device intelligence - it handles different vendor prompts, pagination ('--More--'), enable passwords automatically. It's higher-level and easier to use for network automation."

#### 2. TextFSM (Parse Command Output)

**What it is:** Converts unstructured text output to structured data

```python
from netmiko import ConnectHandler

device = ConnectHandler(**device_info)

# Without TextFSM - raw text
output = device.send_command('show ip interface brief')
# Returns multi-line string, hard to parse

# With TextFSM - structured data
output = device.send_command('show ip interface brief', use_textfsm=True)
# Returns list of dictionaries:
# [
#   {'interface': 'GigabitEthernet0/0', 'ip': '192.168.1.1', 'status': 'up'},
#   {'interface': 'GigabitEthernet0/1', 'ip': '10.0.0.1', 'status': 'up'}
# ]

# Now easy to process
for interface in output:
    if interface['status'] == 'up':
        print(f"{interface['interface']} is UP with IP {interface['ip']}")
```

#### 3. NAPALM (Vendor-Agnostic Library)

**What it is:** Unified API for multiple vendors

```python
from napalm import get_network_driver

# Same code works for Cisco, Juniper, Arista!
driver = get_network_driver('ios')  # or 'junos', 'eos', 'nxos'
device = driver('192.168.1.1', 'admin', 'cisco')

device.open()

# Get facts (same across all vendors)
facts = device.get_facts()
print(facts['hostname'])
print(facts['uptime'])

# Get interfaces (same structure for all vendors)
interfaces = device.get_interfaces()

# Configuration management
config = device.get_config()  # Get current config
device.load_replace_candidate(filename='new_config.txt')  # Stage new config
diff = device.compare_config()  # See what will change
device.commit_config()  # Apply changes
# or device.discard_config()  # Rollback

device.close()
```

### My Network Monitor Script Explained

```python
# scripts/network_monitor.py
import netmiko
from netmiko import ConnectHandler
import time
import json
from datetime import datetime

class NetworkMonitor:
    """Network device monitoring class"""

    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.devices = self.load_inventory()

    def check_device_health(self, device_info):
        """Check health of a single device"""
        try:
            # Connect to device
            connection = ConnectHandler(**device_info)

            # Get interface status (structured data)
            interfaces = connection.send_command(
                'show ip interface brief',
                use_textfsm=True
            )

            # Count up/down interfaces
            total_interfaces = len(interfaces)
            up_interfaces = sum(1 for iface in interfaces
                              if iface.get('status', '').lower() == 'up')

            # Get CPU usage
            cpu_output = connection.send_command('show processes cpu | include CPU')
            cpu_usage = self.parse_cpu_usage(cpu_output)

            # Get memory
            memory_output = connection.send_command('show memory statistics')
            memory_usage = self.parse_memory_usage(memory_output)

            connection.disconnect()

            # Return structured health data
            return {
                'device': device_info['host'],
                'status': 'healthy',
                'reachable': True,
                'timestamp': datetime.now().isoformat(),
                'interfaces': {
                    'total': total_interfaces,
                    'up': up_interfaces,
                    'down': total_interfaces - up_interfaces
                },
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage
            }

        except Exception as e:
            return {
                'device': device_info['host'],
                'status': 'unreachable',
                'reachable': False,
                'error': str(e)
            }

    def parse_cpu_usage(self, cpu_output):
        """Extract CPU percentage from output"""
        # Example output: "CPU utilization for five seconds: 5%/0%"
        try:
            if 'five seconds' in cpu_output:
                parts = cpu_output.split(':')[1].split('/')[0]
                return float(parts.strip().replace('%', ''))
        except:
            pass
        return 0.0

    def monitor_all_devices(self):
        """Monitor all devices in inventory"""
        results = []

        for device in self.devices:
            result = self.check_device_health(device)
            results.append(result)

            # Print real-time status
            symbol = "✓" if result['reachable'] else "✗"
            print(f"{device['host']}: {symbol}")

        return results
```

**Why this approach is good:**
1. **Object-Oriented:** Organized in a class
2. **Error Handling:** Try-except prevents crashes
3. **Structured Data:** Returns dictionaries, not strings
4. **Reusable:** Can import and use in other scripts
5. **Professional:** Docstrings, type hints (could add)

---

## Common Interview Questions

### General Network Engineering

**Q1: "Walk me through how you troubleshoot network connectivity."**

**Answer (Use a systematic approach):**
```
1. Physical Layer (Layer 1):
   - Check cables, link lights, port status
   - Command: show interface status

2. Data Link Layer (Layer 2):
   - Verify correct VLAN
   - Check MAC address table
   - Commands: show vlan, show mac address-table

3. Network Layer (Layer 3):
   - Ping gateway, check IP configuration
   - Verify routing table
   - Commands: show ip interface brief, show ip route, ping

4. Transport Layer (Layer 4):
   - Check if port is open
   - Verify ACLs, firewalls
   - Commands: telnet [ip] [port], show access-lists

5. Application Layer (Layer 7):
   - Test application itself
   - Check application logs
```

**Example:**
"User can't access web server. I start with ping - if that works, it's not Layer 1-3. Then I telnet to port 80 - if that fails, maybe an ACL or firewall blocking. If telnet works, it's the web application itself."

**Q2: "Design a network for a 3-story office building with 100 users."**

**Answer:**
```
Design:
1. Core Layer: 2 routers (redundancy)
   - Routing, inter-VLAN, Internet gateway
   - OSPF for dynamic routing
   - HSRP for gateway redundancy

2. Distribution Layer: 2 switches per floor (redundancy)
   - Layer 3 switches
   - Aggregate access switches
   - VLANs for segmentation

3. Access Layer: Multiple switches per floor
   - Connect end devices
   - Port security enabled
   - DHCP snooping

VLANs:
- VLAN 10: Management (network devices)
- VLAN 20: Data (user computers)
- VLAN 30: Voice (IP phones)
- VLAN 40: Guest WiFi (isolated)
- VLAN 50: Servers (database, file servers)

Security:
- Port security on access switches
- ACLs on router for inter-VLAN rules
- DHCP snooping and DAI (Dynamic ARP Inspection)
- 802.1X for authentication (advanced)

Redundancy:
- Dual routers with HSRP (Hot Standby Router Protocol)
- Dual distribution switches with stacking or VSS
- Dual links (EtherChannel/LACP) between layers
- Dual Internet connections with BGP
```

**Diagram:**
```
           Internet
               |
        [Core Routers] (2x - HSRP)
               |
    [Distribution Switches] (2x per floor)
         /    |    \
   [Access] [Access] [Access]
   Switches per floor
```

**Q3: "What's the difference between Layer 2 and Layer 3 switch?"**

**Answer:**
"**Layer 2 Switch:**
- Operates at Data Link layer
- Forwards based on MAC addresses
- All ports in same broadcast domain (unless VLANs)
- Cannot route between VLANs
- Example: Cisco 2960

**Layer 3 Switch:**
- Operates at Network layer
- Can route between VLANs (inter-VLAN routing)
- Each VLAN is a separate broadcast domain
- Has routing table, can run routing protocols
- Faster than router for inter-VLAN (ASIC hardware)
- Example: Cisco 3850

**When to use:**
- Layer 2: Access layer, just need switching
- Layer 3: Distribution/core, need routing between VLANs"

### Automation-Specific Questions

**Q4: "Why automate networks? What's the ROI?"**

**Answer:**
"**Time Savings:**
- Manual: Configure 100 switches = 2-3 days
- Automated: Configure 100 switches = 5 minutes
- ROI: Save 23 hours * $50/hour = $1,150 per deployment

**Consistency:**
- Manual: 10% error rate (typos, missed steps)
- Automated: <1% error rate (bugs in playbooks)
- ROI: Fewer outages, less troubleshooting time

**Scalability:**
- Manual: Can manage ~50 devices efficiently
- Automated: Can manage 1000+ devices
- ROI: Don't need to hire more engineers as network grows

**Documentation:**
- Manual: Often outdated or missing
- Automated: Code IS the documentation
- ROI: Faster onboarding, better knowledge transfer

**Compliance:**
- Manual: Periodic audits, spreadsheets
- Automated: Continuous compliance checking
- ROI: Pass audits easier, identify issues faster"

**Q5: "What's idempotency and why is it important?"**

**Answer:**
"Idempotency means running the same operation multiple times produces the same result.

**Example (Non-idempotent):**
```python
# BAD - runs every time
connection.send_config_set(['vlan 10'])
# Run twice = VLAN 10 created twice (error!)
```

**Example (Idempotent):**
```yaml
# GOOD - checks if VLAN exists first
- name: Create VLAN 10
  cisco.ios.ios_vlans:
    config:
      - vlan_id: 10
        name: DATA
    state: merged
# Run twice = VLAN 10 only created if missing
```

**Why important:**
1. **Safe to re-run:** Network issues? Just run again
2. **Predictable:** Always get to desired state
3. **Production-safe:** Won't break existing configs
4. **CI/CD friendly:** Can run automatically"

**Q6: "How do you handle rollback if automation fails?"**

**Answer:**
"Multi-layered approach:

**1. Pre-change Backup:**
```yaml
- name: Backup config before changes
  cisco.ios.ios_config:
    backup: yes
    backup_options:
      filename: "{{ inventory_hostname }}_pre_change.cfg"
```

**2. Check Mode (Dry Run):**
```bash
ansible-playbook playbook.yml --check  # Show what WOULD change
```

**3. Configuration Archiving (on device):**
```
archive
 path flash:archive-config
 maximum 14
 write-memory
```

**4. Manual Rollback Playbook:**
```yaml
- name: Restore configuration
  cisco.ios.ios_config:
    src: "backups/{{ inventory_hostname }}_good.cfg"
    replace: config
```

**5. Git Version Control:**
- Every config change is a commit
- Can revert to any previous version
- Shows who changed what and when

**6. Testing Strategy:**
```
Dev → Lab → Staging → Production
Always test in lab first!
```"

---

## Live Demo Scenarios

### Scenario 1: Configure VLANs Across Multiple Switches

**Interviewer:** "Show me how you would deploy VLANs to 10 switches."

**Your Demo:**

```bash
# 1. Show the inventory
cat inventory/lab/hosts

# Output:
[switches]
switch1 ansible_host=192.168.1.11
switch2 ansible_host=192.168.1.12
...

# 2. Show the VLAN definitions
cat vars/vlans.yml

# Output:
vlans:
  - id: 10
    name: Management
  - id: 20
    name: Data
  ...

# 3. Show the playbook
cat playbooks/configure_vlans.yml

# Explain: "This playbook reads VLAN definitions and applies them to all switches"

# 4. Syntax check first
ansible-playbook playbooks/configure_vlans.yml --syntax-check
# Output: playbook: playbooks/configure_vlans.yml

# 5. Dry run (check mode)
ansible-playbook playbooks/configure_vlans.yml --check
# Explain: "This shows what WOULD change without actually changing it"

# 6. Run on single switch first
ansible-playbook playbooks/configure_vlans.yml --limit switch1
# Explain: "Test on one switch before rolling to all"

# 7. Verify on the switch
ansible switches -m cisco.ios.ios_command -a "commands='show vlan brief'"

# 8. Run on all switches
ansible-playbook playbooks/configure_vlans.yml
```

**Narration:**
"This demonstrates my systematic approach:
1. Define configuration as data (vars)
2. Write reusable playbook
3. Test with syntax check
4. Test with dry run
5. Test on one device
6. Verify manually
7. Deploy to all

This is how we safely deploy to production."

### Scenario 2: Backup All Device Configurations

**Interviewer:** "How would you backup configurations from all devices?"

**Your Demo:**

```bash
# Run backup playbook
ansible-playbook playbooks/backup_configs.yml

# Output shows:
PLAY [Backup Network Device Configurations]
TASK [Create backup directory]... changed
TASK [Backup running configuration]... changed: [router1]
TASK [Backup running configuration]... changed: [switch1]
...
TASK [Display summary]
ok: [localhost] => {
    "msg": [
        "Backup Location: ../configs/backups/20241030_120000",
        "Total Devices Backed Up: 10"
    ]
}

# Show the backed up files
ls configs/backups/20241030_120000/

# Output:
router1_running.cfg
router1_startup.cfg
switch1_running.cfg
switch1_startup.cfg
MANIFEST.txt

# Show one config file
head -20 configs/backups/20241030_120000/router1_running.cfg

# Output shows actual device configuration
```

**Narration:**
"Backups are automated nightly via cron:
```
0 2 * * * cd /ansible && ansible-playbook playbooks/backup_configs.yml
```

Backups are versioned and stored for 90 days. If disaster strikes, I can restore any device in under 5 minutes using the restore playbook."

### Scenario 3: Network Health Check

**Interviewer:** "How do you monitor network health?"

**Your Demo:**

```bash
# Run Python monitoring script
python scripts/network_monitor.py

# Output:
=====================================================
