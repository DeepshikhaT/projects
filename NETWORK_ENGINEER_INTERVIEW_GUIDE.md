# Network Engineer Interview Guide (10+ Years Experience - Senior/Staff Level)

## 📚 Table of Contents
1. [Core Knowledge Expected](#core-knowledge-expected)
2. [Technical Interview Questions](#technical-interview-questions)
3. [Troubleshooting Scenarios](#troubleshooting-scenarios)
4. [Design Questions](#design-questions)
5. [Automation & Scripting](#automation--scripting)
6. [Behavioral Questions](#behavioral-questions)
7. [Company-Specific Prep](#company-specific-prep)

---

## Core Knowledge Expected

### For 10+ Years Experience (Senior/Staff Level), You Should Know:

**Advanced Expertise Expected:**
- Deep understanding of all protocols
- Design large-scale networks from scratch
- Lead architecture decisions
- Mentor junior engineers
- Troubleshoot complex multi-vendor environments
- Strong automation and scripting abilities

**Networking Fundamentals:**
- OSI Model (all 7 layers) - explain any layer on demand
- TCP/IP Model
- Subnetting (VLSM, CIDR) - calculate in your head
- IP addressing (IPv4 and IPv6 basics)
- NAT/PAT concepts
- DNS fundamentals

**Routing:**
- Static routing
- Default routes
- OSPF (areas, LSA types, neighbor formation)
- BGP basics (AS numbers, eBGP vs iBGP)
- Route redistribution concepts

**Switching:**
- VLANs (trunking, tagging, native VLAN)
- STP (Spanning Tree Protocol)
- EtherChannel/LACP
- Port security
- VTP (VLAN Trunking Protocol)

**Security:**
- ACLs (Standard vs Extended)
- Port security
- DHCP snooping
- Dynamic ARP Inspection
- Basic firewall concepts

**Wireless (if applicable):**
- SSID, encryption (WPA2/WPA3)
- 2.4GHz vs 5GHz
- Basic RF concepts

**Monitoring & Troubleshooting:**
- SNMP
- Syslog
- NetFlow/sFlow
- Basic Wireshark usage
- Common CLI commands

---

## Technical Interview Questions

### Level 1: Fundamental Questions

**Q1: Explain the OSI Model.**

**Expected Answer:**
```
The OSI Model has 7 layers:

Layer 7 - Application: End-user applications (HTTP, FTP, SMTP)
Layer 6 - Presentation: Data formatting, encryption (SSL/TLS)
Layer 5 - Session: Session management
Layer 4 - Transport: End-to-end communication (TCP/UDP, ports)
Layer 3 - Network: Logical addressing, routing (IP, OSPF, BGP)
Layer 2 - Data Link: MAC addresses, switching (Ethernet, VLANs)
Layer 1 - Physical: Physical transmission (cables, signals)

Mnemonic: "All People Seem To Need Data Processing"
         or "Please Do Not Throw Sausage Pizza Away"
```

**Why it matters:** Every network issue maps to an OSI layer. Shows systematic thinking.

---

**Q2: What happens when you type www.google.com in browser?**

**Expected Answer:**
```
1. DNS Resolution:
   - Browser checks cache
   - Queries DNS server (UDP port 53)
   - DNS returns IP address (e.g., 142.250.80.46)

2. TCP Connection (Layer 4):
   - Three-way handshake: SYN → SYN-ACK → ACK
   - Establishes connection to port 80 (HTTP) or 443 (HTTPS)

3. Routing (Layer 3):
   - Packets routed through multiple hops
   - Each router uses routing table to forward
   - TTL decrements at each hop

4. HTTP Request (Layer 7):
   - Browser sends GET request
   - Google server processes
   - Sends back HTML/CSS/JavaScript

5. Display:
   - Browser renders the page

At each step: ARP resolves MAC addresses, switches forward frames, 
routers route packets.
```

**Why it matters:** Shows understanding of entire network stack.

---

**Q3: Explain subnetting with example.**

**Expected Answer:**
```
Subnetting divides a network into smaller networks.

Example: Given 192.168.1.0/24, create 4 subnets

Step 1: Calculate subnet bits needed
- 4 subnets = 2² = need 2 bits
- New mask: /24 + 2 = /26

Step 2: Calculate subnet size
- 32 - 26 = 6 host bits
- 2⁶ = 64 addresses per subnet
- Usable hosts: 64 - 2 = 62 (minus network & broadcast)

Step 3: List subnets
- Subnet 1: 192.168.1.0/26   (hosts: .1 - .62)
- Subnet 2: 192.168.1.64/26  (hosts: .65 - .126)
- Subnet 3: 192.168.1.128/26 (hosts: .129 - .190)
- Subnet 4: 192.168.1.192/26 (hosts: .193 - .254)

Subnet mask: 255.255.255.192
```

**Practice:** Be ready to subnet on whiteboard!

---

**Q4: TCP vs UDP - when to use each?**

**Expected Answer:**
```
TCP (Transmission Control Protocol):
- Connection-oriented (three-way handshake)
- Reliable (acknowledgments, retransmission)
- Ordered delivery
- Flow control and congestion control
- Slower due to overhead

Use cases:
- HTTP/HTTPS (web browsing)
- FTP (file transfer)
- SSH (remote access)
- Email (SMTP, IMAP)

UDP (User Datagram Protocol):
- Connectionless (fire and forget)
- Unreliable (no acknowledgments)
- No ordering guarantee
- No flow control
- Faster, less overhead

Use cases:
- DNS (queries)
- DHCP (address assignment)
- VoIP (voice calls) - real-time, some loss OK
- Video streaming
- Gaming - speed > reliability
- SNMP (monitoring)

Key difference: TCP = reliable but slow, UDP = fast but best-effort
```

---

**Q5: What is VLAN and why use it?**

**Expected Answer:**
```
VLAN (Virtual LAN) = Logical segmentation of a physical network

Why use VLANs:
1. Security: Separate guest WiFi from corporate network
2. Performance: Reduce broadcast domain size
3. Organization: Group by department/function (not location)
4. Flexibility: Move users between VLANs without physical changes

Example:
Physical: 1 switch, 48 ports
Logical: 
- VLAN 10 (HR): Ports 1-12
- VLAN 20 (Engineering): Ports 13-24
- VLAN 30 (Guest): Ports 25-36

Configuration:
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
 description HR Department

Trunk ports (between switches):
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 switchport trunk native vlan 99
```

**Follow-up Q:** "What's native VLAN?"
**A:** VLAN for untagged traffic on trunk port. Best practice: Change from default VLAN 1 for security.

---

### Level 2: Routing Protocol Questions

**Q6: Explain OSPF.**

**Expected Answer:**
```
OSPF (Open Shortest Path First):
- Link-state routing protocol
- Uses Dijkstra's SPF algorithm
- Metric: Cost (based on bandwidth)
- Administrative Distance: 110

Key Concepts:

1. Areas:
   - Area 0 = Backbone (all areas must connect to it)
   - Regular areas: Area 1, 2, 3, etc.
   - Reduces routing table size, limits LSA flooding

2. Router Types:
   - Internal Router: All interfaces in same area
   - ABR (Area Border Router): Connects multiple areas
   - ASBR (AS Boundary Router): Connects to external networks
   - Backbone Router: Has interface in Area 0

3. Neighbor States:
   Down → Init → 2-Way → ExStart → Exchange → Loading → Full
   
4. LSA Types (main ones):
   - Type 1: Router LSA
   - Type 2: Network LSA
   - Type 3: Summary LSA (ABR advertisement)
   - Type 5: External LSA (ASBR advertisement)

5. Configuration Example:
router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.255.255 area 0
 network 192.168.1.0 0.0.0.255 area 1

Why OSPF:
- Fast convergence (compared to RIP)
- Scalable (areas support large networks)
- No hop count limit
- Supports VLSM
```

**Follow-up Q:** "How does OSPF calculate cost?"
**A:** Cost = Reference Bandwidth / Interface Bandwidth
Default reference = 100 Mbps, so FastEthernet cost = 1, GigE also = 1 (should adjust reference to 10000)

---

**Q7: OSPF vs BGP - when to use each?**

**Expected Answer:**
```
OSPF:
- Interior Gateway Protocol (IGP)
- Within your organization
- Link-state protocol
- Fast convergence
- Metric: Cost (bandwidth-based)
- Max ~1000 routers per area

Use OSPF for:
- Campus networks
- Data center internal routing
- Enterprise WAN (MPLS)

BGP:
- Exterior Gateway Protocol (EGP)
- Between organizations/ISPs
- Path vector protocol
- Slow convergence (stability over speed)
- Metric: AS path (+ many other attributes)
- Internet routing (~1 million routes)

Use BGP for:
- ISP networks
- Multi-homing (multiple ISPs)
- Internet routing
- Large enterprises connecting to internet

Real Example:
Company with offices in 10 cities:
- Internal routing between offices: OSPF
- Connection to internet via 2 ISPs: BGP
- BGP advertises company's public IPs
- OSPF handles internal traffic
```

---

**Q8: What is STP and why do we need it?**

**Expected Answer:**
```
STP (Spanning Tree Protocol) prevents Layer 2 loops

Why loops are bad:
1. Broadcast Storm: Broadcasts loop forever, crash network
2. MAC Table Instability: Switches confused about where hosts are
3. Multiple Frame Copies: Same frame delivered multiple times

How STP works:

1. Elect Root Bridge:
   - Lowest Bridge Priority (default 32768) + MAC
   - All ports forwarding

2. Each switch calculates:
   - Root Port: Best path to root bridge (forwarding)
   - Designated Port: Best path on each segment (forwarding)
   - Blocked Port: Alternate paths (blocking to prevent loops)

3. Port States:
   - Blocking (20 sec): Receives BPDUs only
   - Listening (15 sec): Processes BPDUs
   - Learning (15 sec): Learns MAC addresses
   - Forwarding: Normal operation
   - Convergence time: ~50 seconds (too slow!)

Modern Alternatives:
- RSTP (Rapid STP): Converges in < 6 seconds
- PVST+ (Cisco): One STP instance per VLAN
- MSTP: Multiple VLANs per STP instance

Configuration:
spanning-tree mode rapid-pvst
spanning-tree vlan 1-100 priority 4096  ! Make this switch root

Verification:
show spanning-tree
show spanning-tree interface gi0/1
```

**Follow-up Q:** "What is BPDU?"
**A:** Bridge Protocol Data Unit - messages switches exchange to elect root bridge and detect topology changes.

---

### Level 3: Advanced Questions

**Q9: Explain NAT and its types.**

**Expected Answer:**
```
NAT (Network Address Translation):
Translates private IPs to public IPs (and vice versa)

Why NAT:
- IPv4 address exhaustion (only 4 billion addresses)
- Security (hides internal network)
- Cost (need fewer public IPs)

Types:

1. Static NAT (One-to-One):
   Inside: 192.168.1.10 → Outside: 203.0.113.10
   
   Use: Servers that need fixed public IP
   
   Config:
   ip nat inside source static 192.168.1.10 203.0.113.10

2. Dynamic NAT (Many-to-Pool):
   Inside: 192.168.1.0/24 → Outside: Pool of 203.0.113.10-20
   
   Use: Multiple users sharing pool of public IPs
   
   Config:
   ip nat pool PUBLIC 203.0.113.10 203.0.113.20 netmask 255.255.255.0
   ip nat inside source list 1 pool PUBLIC

3. PAT / NAT Overload (Many-to-One):
   Inside: 192.168.1.0/24 → Outside: 203.0.113.5 (using different ports)
   
   Example:
   192.168.1.10:5000 → 203.0.113.5:50001
   192.168.1.11:5000 → 203.0.113.5:50002
   
   Use: Home/office - everyone shares one public IP
   
   Config:
   ip nat inside source list 1 interface gi0/0 overload

NAT Direction:
- Inside: Private network side
- Outside: Public/Internet side

Troubleshooting:
show ip nat translations
show ip nat statistics
debug ip nat
```

---

**Q10: How does ARP work?**

**Expected Answer:**
```
ARP (Address Resolution Protocol):
Resolves IP address to MAC address (Layer 3 → Layer 2)

Scenario: PC1 (10.0.0.10) wants to ping PC2 (10.0.0.20)

Step 1: PC1 checks ARP cache
Command: arp -a
If 10.0.0.20 not in cache → need ARP

Step 2: PC1 sends ARP Request (broadcast)
Source MAC: PC1 MAC
Dest MAC: FF:FF:FF:FF:FF:FF (broadcast)
Message: "Who has 10.0.0.20? Tell 10.0.0.10"

Step 3: All devices receive broadcast
PC2 recognizes its IP, others ignore

Step 4: PC2 sends ARP Reply (unicast)
Source MAC: PC2 MAC
Dest MAC: PC1 MAC
Message: "10.0.0.20 is at MAC: AA:BB:CC:DD:EE:FF"

Step 5: PC1 updates ARP cache
Now knows: 10.0.0.20 = AA:BB:CC:DD:EE:FF

Step 6: PC1 sends ping
Can now build Ethernet frame with correct dest MAC

ARP Cache Timeout: 
- Windows: 2 minutes (dynamic), 10 minutes (static)
- Cisco: 4 hours

Gratuitous ARP:
- Device announces own IP/MAC (detects conflicts)
- Updates ARP caches when MAC changes

Security: ARP Spoofing
- Attacker sends fake ARP replies
- Redirects traffic through attacker
- Defense: Dynamic ARP Inspection (DAI)
```

---

## Troubleshooting Scenarios

### Scenario 1: Users Can't Access Internet

**Interviewer:** "Users in VLAN 10 can't browse internet. Walk me through your troubleshooting."

**Your Answer (Systematic Approach):**

```
Use bottom-up approach (OSI Model):

1. PHYSICAL LAYER (Layer 1):
   ✓ Check: Are PCs physically connected?
   Command: Check link lights
   Test: Ping default gateway (10.0.10.1)
   
2. DATA LINK LAYER (Layer 2):
   ✓ Check: Correct VLAN assignment?
   Command: show vlan brief
   Expected: Ports in VLAN 10
   Test: Can devices in same VLAN talk to each other?
   
3. NETWORK LAYER (Layer 3):
   ✓ Check: Do PCs have correct IP?
   Command: ipconfig (Windows) or ifconfig (Linux)
   Expected: 10.0.10.0/24 range, gateway 10.0.10.1
   
   ✓ Check: Can PC reach gateway?
   Test: ping 10.0.10.1
   If fails → problem between PC and router
   
   ✓ Check: Does gateway have route to internet?
   Command (on router): show ip route
   Expected: Default route (0.0.0.0/0)
   
   ✓ Check: Can gateway reach internet?
   Test: ping 8.8.8.8 from router
   
4. Check NAT:
   ✓ Command: show ip nat translations
   Expected: See inside to outside translations
   
   ✓ Check NAT config:
   - Is interface marked "ip nat inside"?
   - Is internet interface marked "ip nat outside"?
   - Is ACL permitting VLAN 10 traffic?
   
5. Check DNS:
   ✓ Test: ping google.com (if fails but ping 8.8.8.8 works → DNS issue)
   Command: nslookup google.com
   Check: Are DNS servers configured? (8.8.8.8, 8.8.4.4)
   
6. Check Security:
   ✓ ACLs blocking?
   Command: show access-lists
   ✓ Firewall rules?

Common Issues Found:
- NAT not configured for VLAN 10
- ACL blocking VLAN 10
- No default route on router
- DNS not configured on PCs
- Router interface down
```

**Show your thinking process** - systematic, layer by layer!

---

### Scenario 2: OSPF Neighbors Not Forming

**Interviewer:** "Two routers won't form OSPF neighbor relationship. Troubleshoot."

**Your Answer:**

```
Systematic checks:

1. BASIC CONNECTIVITY:
   ✓ Can routers ping each other?
   Test: ping neighbor IP
   If fails → Layer 1/2 issue (cable, interface down)

2. OSPF ENABLED:
   ✓ Command: show ip protocols
   Expected: "Routing Protocol is ospf 1"
   
   ✓ Check: Is OSPF running on interface?
   Command: show ip ospf interface
   Expected: Interface listed with area

3. OSPF CONFIGURATION MATCH:
   ✓ Same Area? (must match!)
   ✓ Same Subnet? (interfaces must be in same subnet)
   ✓ Not passive? (passive-interface blocks hellos)
   
   Command: show ip ospf interface gi0/0
   Look for: "Passive interface: No"

4. AUTHENTICATION MATCH:
   ✓ If one router has authentication, both must match
   ✓ Same authentication type and key
   
   Check: show ip ospf interface
   Look for: "Message digest authentication enabled"

5. TIMERS MATCH:
   ✓ Hello interval (default 10 sec)
   ✓ Dead interval (default 40 sec)
   
   Command: show ip ospf interface
   Must match on both routers!

6. MTU MATCH:
   ✓ MTU mismatch = stuck in EXSTART state
   Command: show interfaces
   Look for: MTU value (should be 1500)
   
   Fix: ip mtu 1500

7. ACCESS LISTS:
   ✓ Check if ACL blocking OSPF
   OSPF uses protocol number 89
   
   Command: show ip access-lists
   Ensure: permit ip any any or specific permit for OSPF

8. CHECK NEIGHBOR STATE:
   Command: show ip ospf neighbor
   
   States:
   - Not appearing → no hellos received
   - INIT → receiving hellos but not seeing own RID
   - 2-WAY → normal for DROther on broadcast network
   - EXSTART → MTU mismatch!
   - EXCHANGE/LOADING → normal during adjacency
   - FULL → success!

9. DEBUG (CAREFULLY):
   Command: debug ip ospf adj
   Shows: OSPF adjacency process in real-time
   Remember: undebug all when done!

Common Solutions:
1. Fix subnet mismatch
2. Remove passive-interface
3. Match authentication
4. Fix MTU mismatch
5. Correct area mismatch
```

---

### Scenario 3: Slow Network Performance

**Interviewer:** "Users complaining network is slow. How do you troubleshoot?"

**Your Answer:**

```
Systematic performance troubleshooting:

1. SCOPE THE PROBLEM:
   Questions to ask:
   - All users or specific group?
   - All applications or specific ones?
   - All day or specific times?
   - Started when? (recent changes?)

2. CHECK INTERFACE UTILIZATION:
   Command: show interface gi0/1
   Look for:
   - "load" percentage (high = congested)
   - Input/output rate
   
   Calculation:
   If 90%+ utilization → need more bandwidth

3. CHECK ERRORS:
   Command: show interface gi0/1
   
   Look for:
   a. CRC Errors:
      - Bad cable or port
      - Fix: Replace cable, try different port
   
   b. Input/Output Errors:
      - Duplex mismatch (one side auto, other hard-coded)
      - Fix: Match duplex settings
   
   c. Collisions:
      - Duplex mismatch on half-duplex
      - Fix: Use full-duplex
   
   d. Drops:
      - Queue full (congestion)
      - Fix: Increase bandwidth or enable QoS

4. CHECK DUPLEX MISMATCH:
   Command: show interfaces status
   
   One side: auto/auto
   Other side: 100/full (hard-coded)
   = MISMATCH!
   
   Symptoms:
   - Slow performance
   - Many errors
   - Intermittent connectivity
   
   Fix: Match both sides (both auto or both hard-coded)

5. CHECK FOR LOOPS:
   Command: show spanning-tree inconsistentports
   
   Loop symptoms:
   - Very high CPU
   - Network comes and goes
   - Broadcast storm
   
   Fix: Check STP, fix redundant links

6. CHECK CPU/MEMORY ON DEVICES:
   Command: show processes cpu
   Command: show memory
   
   High CPU causes:
   - Routing protocol issues
   - Loops
   - DOS attack
   
   Low memory:
   - Memory leak
   - Too many routes
   - Device undersized

7. CHECK QoS (if configured):
   Command: show policy-map interface gi0/1
   
   Verify: Voice traffic prioritized over data

8. PACKET CAPTURE:
   If all else fails, capture traffic:
   
   Wireshark filter examples:
   - tcp.analysis.retransmission (find retransmissions)
   - tcp.analysis.window_full (buffer issues)
   - icmp.type == 3 (destination unreachable)

9. CHECK BANDWIDTH USAGE:
   Tools:
   - NetFlow (Cisco)
   - sFlow
   - SNMP monitoring (MRTG, Cacti)
   
   Find: Which applications/users using bandwidth?

10. TEST FROM DIFFERENT POINTS:
    - Test between VLANs
    - Test within same VLAN
    - Test to internet
    - Isolates where problem is

Common Findings:
1. Duplex mismatch (very common!)
2. Bad cable
3. Bandwidth saturation
4. Broadcast storm / loop
5. Application issue (not network)
```

---

## Design Questions

### Question 1: Design Network for 3-Floor Office

**Interviewer:** "Design network for 3-floor office building, 100 users per floor."

**Your Answer:**

```
Design Approach:

1. HIERARCHICAL MODEL:

   CORE LAYER (Top):
   - 2x Core Switches (redundancy)
   - Layer 3 switches
   - Handle inter-VLAN routing
   - Routing protocols (OSPF)
   - Connect to internet gateway routers
   
   DISTRIBUTION LAYER (Middle):
   - 2x Distribution switches per floor (6 total)
   - Layer 3 capable
   - Aggregate access switches
   - VLANs terminate here
   - Link aggregation to core (redundancy)
   
   ACCESS LAYER (Bottom):
   - 4-6 switches per floor (depends on port density)
   - Layer 2 switches (cost-effective)
   - Connect end-user devices
   - 48 ports per switch typical
   
2. VLAN DESIGN:
   - VLAN 10: Management (network devices)
   - VLAN 20: Data (user computers)
   - VLAN 30: Voice (IP phones)
   - VLAN 40: Guest (visitor WiFi)
   - VLAN 50: Printers/Servers
   - VLAN 99: Native (unused VLAN for security)

3. IP ADDRESSING:
   - VLAN 10: 192.168.10.0/24 (Management)
   - VLAN 20: 10.0.0.0/16 (Data - large, 65k hosts)
   - VLAN 30: 10.1.0.0/24 (Voice)
   - VLAN 40: 10.2.0.0/24 (Guest)
   - VLAN 50: 10.3.0.0/24 (Servers)

4. REDUNDANCY:
   - Dual core switches (HSRP/VRRP for gateway redundancy)
   - Dual distribution per floor
   - EtherChannel/LACP for link aggregation
   - STP for loop prevention
   - Dual internet connections (BGP for multi-homing)

5. SECURITY:
   - Port security on access ports
   - DHCP snooping
   - Dynamic ARP Inspection
   - IP Source Guard
   - ACLs between VLANs
   - 802.1X authentication (optional)

6. WIRELESS:
   - 3-4 APs per floor (coverage planning)
   - Wireless controller (centralized management)
   - Multiple SSIDs (Corporate, Guest)
   - Guest network isolated (VLAN 40)

7. INTERNET CONNECTIVITY:
   - 2x Firewall/Router (active-standby)
   - Dual ISP connections
   - BGP for load balancing and failover
   - NAT for internal network

Diagram:
```
            Internet
               |
        [Dual Firewalls]
               |
        [Core Switches] (2x, redundant)
         /     |     \
    [Dist]  [Dist]  [Dist] (2 per floor)
     /  \    /  \    /  \
  [Access Switches] (48-port, multiple per floor)
     |  |  |  |  |  |
   [Users, Phones, APs]
```

Estimated Equipment:
- 2x Core switches
- 6x Distribution switches
- 12-18x Access switches
- 2x Routers/Firewalls
- 10-12x Wireless APs
```

---

## Automation & Scripting

### What Employers Expect for 3 Years Experience

**Basic Level:**
- Can write simple Python/Bash scripts
- Understand APIs and REST
- Basic Ansible playbooks
- Read and modify existing automation

**You Should Know:**

**Python for Networking:**
```python
# Example: Backup all switch configs

import netmiko
from netmiko import ConnectHandler
import datetime

devices = [
    {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
    },
    # ... more devices
]

def backup_device(device):
    """Backup configuration from device"""
    try:
        connection = ConnectHandler(**device)
        config = connection.send_command('show running-config')
        
        filename = f"backup_{device['host']}_{datetime.date.today()}.cfg"
        with open(filename, 'w') as f:
            f.write(config)
        
        connection.disconnect()
        print(f"✓ Backed up {device['host']}")
        return True
    except Exception as e:
        print(f"✗ Failed {device['host']}: {e}")
        return False

# Backup all devices
for device in devices:
    backup_device(device)
```

**Interview Questions:**

**Q: "Have you automated any network tasks?"**

**Answer:** (Based on your experience)
```
"Yes, in my previous roles I've automated several tasks:

1. Configuration Backups:
   - Python script using Netmiko
   - Runs nightly via cron
   - Backs up all router/switch configs
   - Saves to Git for version control

2. Network Monitoring:
   - Python script that checks device health
   - Monitors CPU, memory, interface status
   - Sends alerts via email/Slack
   - Logs data to database for trending

3. VLAN Provisioning (Ansible):
   - Ansible playbook for adding VLANs
   - Define VLANs in YAML file
   - Deploy to multiple switches
   - Consistent configuration

Benefits:
- Saves time (hours → minutes)
- Reduces errors (no typos)
- Repeatable and scalable
- Documented (code is documentation)"
```

**Q: "What's the difference between Ansible and Python for network automation?"**

**Answer:**
```
Python (Netmiko/Paramiko):
- More flexible/powerful
- Better for complex logic
- Can do anything programming allows
- Steeper learning curve
- Best for: Custom scripts, data processing

Ansible:
- Easier to learn (YAML, no coding)
- Idempotent (safe to run multiple times)
- Built-in modules for common tasks
- Less flexible than Python
- Best for: Configuration management, deployments

My approach:
- Use Ansible for: Standard configs, deployments
- Use Python for: Monitoring, data collection, complex logic

Example:
- Deploy VLANs → Ansible (standard task)
- Analyze NetFlow data → Python (complex analysis)
```

---

## Behavioral Questions

### Common Questions for Network Engineers

**Q: "Tell me about a time you troubleshot a difficult network issue."**

**STAR Method Answer:**

**Situation:**
"In my previous role, we had intermittent connectivity issues affecting ~50 users. Users would lose connection for 5-10 seconds every few minutes."

**Task:**
"My task was to identify root cause and resolve it quickly as it was affecting productivity."

**Action:**
"I took a systematic approach:
1. Gathered information - which users, when, which applications
2. Checked for patterns - all users in same VLAN (VLAN 20)
3. Checked switch logs - saw repeated 'port flapping' messages
4. Checked spanning-tree - found root bridge election flapping
5. Discovered: New switch added without configuring STP priority
6. New switch kept becoming root bridge, causing topology changes

Solution:
- Set proper STP priorities on all switches
- Configured BPDU guard on access ports
- Added port-fast for user ports
- Issue resolved immediately"

**Result:**
"Problem solved in 2 hours. Implemented STP best practices across network to prevent recurrence. Documented the issue and solution for future reference."

---

**Q: "Describe a time you disagreed with a colleague. How did you handle it?"**

**Answer:**
"A colleague wanted to implement a flat network (no VLANs) for simplicity. I believed VLANs were necessary for security and performance.

I approached it professionally:
1. Asked to understand their perspective (why flat network?)
2. Explained my concerns (security, broadcast domains)
3. Proposed compromise: Start with minimal VLANs, add as needed
4. Created proof-of-concept showing benefits
5. We agreed on design with 4 VLANs (not flat, but not overly complex)

Outcome: Implementation went smoothly, colleague appreciated the collaborative approach, and we achieved good balance between security and simplicity."

---

**Q: "How do you stay updated with networking technologies?"**

**Answer:**
"I actively invest in learning:

1. Certifications: Working toward CCNP (have CCNA)
2. Online Learning: Udemy, Pluralsight courses
3. Community: 
   - Reddit (r/networking, r/ccna)
   - Network engineering forums
   - Local networking meetups
4. Hands-on: Home lab with GNS3/EVE-NG
5. Reading: Cisco blogs, network engineering websites
6. Projects: Build automation tools (like in my GitHub)

Recent topics I've studied:
- SD-WAN concepts
- Network automation (Ansible, Python)
- BGP advanced features
- Network security best practices"

---

## Company-Specific Prep

### For DNS Engineer Role (Cloudflare)

**Key Knowledge Areas:**

1. **DNS Fundamentals (MUST KNOW):**

### DNS Record Types - Complete Explanation

**A Record (Address Record)**
```
Purpose: Maps domain name to IPv4 address
Example:
  example.com.    3600    IN    A    192.0.2.1
  www.example.com. 3600    IN    A    192.0.2.1

Breakdown:
- example.com. = Domain name (dot at end is important!)
- 3600 = TTL (Time To Live) in seconds (1 hour)
- IN = Internet class
- A = Record type
- 192.0.2.1 = IPv4 address

Use Case: Basic website hosting
When user types www.example.com, browser gets 192.0.2.1

Multiple A Records (Round Robin Load Balancing):
  example.com.    IN    A    192.0.2.1
  example.com.    IN    A    192.0.2.2
  example.com.    IN    A    192.0.2.3
```

**AAAA Record (IPv6 Address)**
```
Purpose: Maps domain name to IPv6 address
Example:
  example.com.    IN    AAAA    2001:0db8::1

IPv6 Address Format:
- 8 groups of 4 hexadecimal digits
- :: = compress consecutive zeros
- 2001:0db8:0000:0000:0000:0000:0000:0001
- Shortened: 2001:0db8::1

Use Case: IPv6-enabled websites
Future-proofing as world transitions to IPv6

Why AAAA?
- A = IPv4 (32 bits = 4 bytes)
- AAAA = IPv6 (128 bits = 4 × 4 bytes)
```

**CNAME Record (Canonical Name)**
```
Purpose: Alias - points one domain to another
Example:
  www.example.com.    IN    CNAME    example.com.
  ftp.example.com.    IN    CNAME    example.com.
  mail.example.com.   IN    CNAME    example.com.

How it works:
1. User queries www.example.com
2. DNS returns CNAME → example.com
3. DNS then queries example.com for A record
4. Returns final IP address

IMPORTANT RULES:
✗ Cannot use CNAME at zone apex (example.com cannot be CNAME)
✗ Cannot mix CNAME with other records at same name
✓ Can chain CNAMEs (but slow, not recommended)

Real-World Example:
  www.example.com.    IN    CNAME    example.com.
  example.com.        IN    A         192.0.2.1

Why use CNAME?
- Central management: Update one A record, all CNAMEs follow
- CDN: Point to CDN hostname
  www.example.com. IN CNAME www.example.cloudfront.net.
```

**MX Record (Mail Exchange)**
```
Purpose: Specifies mail servers for domain
Example:
  example.com.    IN    MX    10    mail1.example.com.
  example.com.    IN    MX    20    mail2.example.com.

Format:
  domain    IN    MX    priority    mail-server

Priority: Lower number = higher priority
- 10 = Primary mail server (try first)
- 20 = Backup mail server (try if 10 fails)

Complete Mail Setup:
  example.com.        IN    MX    10    mail.example.com.
  mail.example.com.   IN    A          192.0.2.10

How Email Works:
1. Send email to user@example.com
2. Sender's mail server queries MX for example.com
3. Gets: mail.example.com (priority 10)
4. Queries A record for mail.example.com
5. Gets: 192.0.2.10
6. Connects to 192.0.2.10 and delivers email

Multiple MX (Redundancy):
  example.com.    IN    MX    10    mail1.example.com.
  example.com.    IN    MX    20    mail2.example.com.
  example.com.    IN    MX    30    mail3.example.com.
```

**TXT Record (Text Record)**
```
Purpose: Store arbitrary text data
Common Uses:

1. SPF (Sender Policy Framework) - Email Authentication:
  example.com.    IN    TXT    "v=spf1 ip4:192.0.2.0/24 include:_spf.google.com ~all"
  
  Meaning:
  - v=spf1: SPF version 1
  - ip4:192.0.2.0/24: Allowed to send from this IP range
  - include:_spf.google.com: Also allow Google's servers
  - ~all: Soft fail for others

2. DKIM (DomainKeys Identified Mail) - Email Signing:
  default._domainkey.example.com.    IN    TXT    "v=DKIM1; k=rsa; p=MIGfMA0G..."
  
  Contains public key for email signature verification

3. DMARC (Domain-based Message Authentication):
  _dmarc.example.com.    IN    TXT    "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
  
  Tells receivers what to do with failed SPF/DKIM

4. Domain Verification (Google, Microsoft):
  example.com.    IN    TXT    "google-site-verification=abc123def456"
  
  Proves you own the domain

5. Site Information:
  example.com.    IN    TXT    "v=verifyme; owner=Company Inc"

Length Limit: 255 characters per string (can have multiple strings)
```

**NS Record (Name Server)**
```
Purpose: Delegates DNS zone to name servers
Example:
  example.com.    IN    NS    ns1.example.com.
  example.com.    IN    NS    ns2.example.com.

What it means:
"For example.com, ask these name servers for information"

Delegation Example:
Parent zone (com.):
  example.com.    IN    NS    ns1.example.com.
  example.com.    IN    NS    ns2.example.com.
  ns1.example.com. IN    A     192.0.2.1
  ns2.example.com. IN    A     192.0.2.2

Subdomain Delegation:
  subdomain.example.com.    IN    NS    ns1.subdomain.example.com.
  subdomain.example.com.    IN    NS    ns2.subdomain.example.com.

Cloudflare Example:
  example.com.    IN    NS    abe.ns.cloudflare.com.
  example.com.    IN    NS    bea.ns.cloudflare.com.

Why Multiple NS Records?
- Redundancy: If one name server down, others work
- Load balancing: Distribute queries
- Best practice: 2-4 name servers
```

**SOA Record (Start of Authority)**
```
Purpose: Contains zone information and settings
Example:
  example.com.    IN    SOA    ns1.example.com. admin.example.com. (
                                2023103101    ; Serial (YYYYMMDDnn)
                                3600          ; Refresh (1 hour)
                                1800          ; Retry (30 minutes)
                                604800        ; Expire (1 week)
                                86400 )       ; Minimum TTL (1 day)

Fields Explained:

1. Primary Name Server: ns1.example.com.
   - Authoritative server for this zone

2. Email: admin.example.com.
   - Contact email (replace @ with .)
   - admin@example.com → admin.example.com.

3. Serial: 2023103101
   - Version number (increment on every change)
   - Format: YYYYMMDDnn (date + sequence)
   - Secondary servers use this to detect updates

4. Refresh: 3600 seconds
   - How often secondary checks for updates
   
5. Retry: 1800 seconds
   - If refresh fails, retry after this time
   
6. Expire: 604800 seconds (1 week)
   - If secondary can't contact primary for this long,
     stop serving the zone
   
7. Minimum TTL: 86400 seconds (1 day)
   - Negative caching (cache NXDOMAIN responses)

Why SOA Matters:
- Required for every DNS zone
- Controls zone transfer behavior
- Affects DNS propagation timing
```

**PTR Record (Pointer - Reverse DNS)**
```
Purpose: Maps IP address to hostname (reverse of A record)
Example:
  1.2.0.192.in-addr.arpa.    IN    PTR    mail.example.com.

How it works:
IP: 192.0.2.1
Reversed: 1.2.0.192
Add suffix: 1.2.0.192.in-addr.arpa.

IPv6 PTR:
  1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.

Use Cases:

1. Email Servers (CRITICAL):
   Many mail servers reject email from IPs without PTR
   PTR must match hostname in HELO/EHLO command
   
   Forward: mail.example.com → 192.0.2.10
   Reverse: 192.0.2.10 → mail.example.com
   ✓ Match = Good
   ✗ No match = Email might be rejected

2. Logging/Troubleshooting:
   Logs show hostnames instead of just IPs

3. Security:
   Some services verify PTR for authenticity

Setting up PTR:
- You DON'T control PTR for your IPs
- Your ISP or hosting provider controls it
- Request them to set PTR for you

Verification:
  dig -x 192.0.2.1
  nslookup 192.0.2.1
```

**SRV Record (Service Record)**
```
Purpose: Specifies location of services
Example:
  _http._tcp.example.com.    IN    SRV    10 60 80 web.example.com.

Format:
  _service._proto.name    IN    SRV    priority weight port target

Fields:
- _service: Service name (e.g., _http, _sip, _ldap)
- _proto: Protocol (e.g., _tcp, _udp)
- priority: Like MX priority (lower = preferred)
- weight: Load balancing (higher = more traffic)
- port: Service port number
- target: Hostname providing the service

Real Examples:

1. Microsoft Active Directory:
  _ldap._tcp.dc._msdcs.example.com.    IN    SRV    0 100 389 dc1.example.com.

2. SIP (VoIP):
  _sip._tcp.example.com.    IN    SRV    10 60 5060 sip1.example.com.
  _sip._tcp.example.com.    IN    SRV    10 40 5060 sip2.example.com.

3. XMPP (Jabber):
  _xmpp-client._tcp.example.com.    IN    SRV    5 0 5222 xmpp.example.com.

Why SRV Records?
- Service discovery without hardcoding ports
- Load balancing across multiple servers
- Failover capabilities
- Used heavily in VoIP, instant messaging, Active Directory
```

**NAPTR Record (Naming Authority Pointer)**
```
Purpose: Advanced DNS rewriting and service selection
Used mainly in telecom (VoIP, ENUM)

Example:
  example.com.    IN    NAPTR    100 10 "U" "E2U+sip" "!^.*$!sip:info@example.com!" .

Format:
  name    IN    NAPTR    order preference flags service regexp replacement

Fields:
- order: Processing order (lower first)
- preference: If order same, use preference
- flags: Processing flags
  - U = Terminal (result is URI)
  - S = Look up SRV record next
  - A = Look up A/AAAA record next
- service: Service type (e.g., E2U+sip for SIP)
- regexp: Regular expression to transform input
- replacement: Replacement pattern or domain

ENUM Example (Phone Number to SIP):
Input: +1-555-123-4567
ENUM domain: 7.6.5.4.3.2.1.5.5.5.1.e164.arpa

  7.6.5.4.3.2.1.5.5.5.1.e164.arpa.    IN    NAPTR    100 10 "u" "E2U+sip" "!^.*$!sip:15551234567@example.com!" .

Result: sip:15551234567@example.com

Real-World Use:
- Telecom: Convert phone numbers to SIP addresses
- VoIP: Route calls based on phone number
- ENUM: E.164 Number Mapping

Why Most People Don't Use NAPTR:
- Complex to configure
- Mainly used in telecom industry
- Requires understanding of regular expressions
- Most websites use simpler A/CNAME records
```

**CAA Record (Certification Authority Authorization)**
```
Purpose: Specify which CAs can issue SSL certificates
Example:
  example.com.    IN    CAA    0 issue "letsencrypt.org"
  example.com.    IN    CAA    0 issuewild "letsencrypt.org"
  example.com.    IN    CAA    0 iodef "mailto:security@example.com"

Format:
  name    IN    CAA    flags tag value

Flags:
- 0 = Non-critical (default)
- 128 = Critical (must understand to proceed)

Tags:
- issue: Which CA can issue certificates
- issuewild: Which CA can issue wildcard certificates
- iodef: Email/URL to report violations

Why CAA?
- Security: Prevent unauthorized certificate issuance
- Required by: Certificate Authorities (per CA/Browser Forum)

Example Configuration:
  example.com.    IN    CAA    0 issue "letsencrypt.org"
  example.com.    IN    CAA    0 issue "digicert.com"
  example.com.    IN    CAA    0 iodef "mailto:security@example.com"

Means:
- Only Let's Encrypt and DigiCert can issue certs
- Notify security@example.com of violations
```

### DNS Query Types and Behavior

**Recursive Query:**
```
Client → Recursive Resolver: "What's www.example.com?"
Resolver does all the work:
1. Queries root servers
2. Queries TLD servers
3. Queries authoritative servers
4. Returns final answer to client

Client just waits for answer.
```

**Iterative Query:**
```
Client → Server: "What's www.example.com?"
Server: "I don't know, ask .com servers at X.X.X.X"
Client → .com servers: "What's www.example.com?"
.com: "I don't know, ask example.com servers at Y.Y.Y.Y"
Client → example.com servers: "What's www.example.com?"
example.com: "It's 192.0.2.1"

Client does the work, following referrals.
```

DNS Query Process:
1. User types www.example.com
2. Check local cache
3. Query recursive resolver (ISP DNS or 8.8.8.8)
4. If not cached, query root servers
5. Root → TLD servers (.com)
6. TLD → Authoritative name server (example.com)
7. Returns A record (IP address)
8. Cache the result (TTL)

DNS Tools:
- nslookup: Basic queries
- dig: Detailed queries (preferred)
- host: Simple queries
- whois: Domain information

Example dig command:
dig www.example.com A
dig example.com MX
dig @8.8.8.8 example.com  # Query specific server
```

2. **DNS Security:**
```
DNSSEC (DNS Security Extensions):
- Prevents DNS spoofing/cache poisoning
- Uses digital signatures
- Chain of trust from root to domain

Common Attacks:
- DNS Cache Poisoning
- DDoS (overwhelm DNS servers)
- DNS Tunneling (data exfiltration)

Mitigation:
- DNSSEC
- Rate limiting
- Anycast (distribute load)
- Response Rate Limiting (RRL)
```

3. **Cloudflare-Specific:**
```
Cloudflare Services:
- CDN (Content Delivery Network)
- DDoS protection
- DNS (1.1.1.1 - fastest DNS resolver)
- Web Application Firewall (WAF)
- Load balancing

Why Cloudflare DNS is fast:
- Anycast network (route to nearest server)
- Global presence (>250 cities)
- Optimized caching
- Modern protocols (DoH, DoT)
```

**Sample Interview Questions:**

**Q: "What happens when you change a DNS record?"**
**A:** 
"When you change a DNS record:
1. Update is made on authoritative server
2. Old cached records remain valid until TTL expires
3. TTL (Time To Live) determines how long caches keep record
4. Lower TTL = faster propagation but more queries
5. Higher TTL = slower updates but less load

Best practice before changing:
- Lower TTL ahead of time (e.g., from 86400 to 300)
- Make change
- Wait for propagation
- Raise TTL back up

Propagation time = Old TTL value (not 24-48 hours as commonly believed)"

---

**Q: "How would you troubleshoot DNS resolution issues?"**
**A:**
```
Step-by-step approach:

1. Verify connectivity:
   ping 8.8.8.8  # Can reach internet?

2. Test DNS resolution:
   nslookup www.google.com
   # If fails, DNS issue

3. Try different DNS server:
   nslookup www.google.com 8.8.8.8
   # If works, problem with configured DNS server

4. Check DNS configuration:
   ipconfig /all  # Windows
   cat /etc/resolv.conf  # Linux
   
5. Flush DNS cache:
   ipconfig /flushdns  # Windows
   sudo systemd-resolve --flush-caches  # Linux

6. Check firewall:
   - UDP port 53 (DNS queries)
   - TCP port 53 (zone transfers, large responses)

7. Use dig for detailed troubleshooting:
   dig www.example.com +trace
   # Shows full resolution path

8. Check authoritative server:
   dig @ns1.example.com example.com
   # Query authoritative directly

Common Issues:
- Wrong DNS server configured
- DNS server down
- Firewall blocking port 53
- ISP DNS issues
- DNSSEC validation failure
```

---

## Final Preparation Tips

### Week Before Interview:

**Day 1-2: Review Fundamentals**
- [ ] OSI Model (explain each layer)
- [ ] Subnetting (practice calculations)
- [ ] Routing basics (static, default routes)
- [ ] Switching basics (VLANs, trunking)

**Day 3-4: Protocol Deep Dive**
- [ ] OSPF (areas, neighbors, LSAs)
- [ ] STP (root bridge, port states)
- [ ] TCP/IP (3-way handshake, flow control)
- [ ] DNS (record types, resolution)

**Day 5: Troubleshooting Practice**
- [ ] Practice 3-5 troubleshooting scenarios
- [ ] Use systematic OSI layer approach
- [ ] Practice explaining thought process out loud

**Day 6: Company Research**
- [ ] Read about company (website, news)
- [ ] Understand their products/services
- [ ] Prepare company-specific questions
- [ ] Review job description keywords

**Day 7: Mock Interview**
- [ ] Practice with friend/recording
- [ ] Answer behavioral questions (STAR method)
- [ ] Practice drawing network diagrams
- [ ] Prepare questions to ask interviewer

### Day of Interview:

**Technical Prep:**
- [ ] Review your resume (be ready to discuss everything)
- [ ] Bring notepad and pen (for diagrams)
- [ ] Prepare 3-5 questions to ask interviewer
- [ ] Review company's network infrastructure (if public)

**Mental Prep:**
- [ ] Get good sleep
- [ ] Arrive 10-15 min early (or test video link)
- [ ] Dress appropriately (business casual minimum)
- [ ] Stay calm - it's okay to say "I don't know but here's how I'd find out"

---

## Your Strengths (Based on Your Experience)

**Nokia (3 years) + Meta (9 months) = Strong Foundation**

**What You Have:**
1. ✅ Real telecom experience (5G automation)
2. ✅ Large-scale networks (Meta's scale)
3. ✅ Automation skills (Python, Ansible)
4. ✅ Cloud experience (deployment automation)
5. ✅ Mix of traditional networking + modern DevOps

**How to Position Yourself:**

**For Network Engineer Roles:**
"I have 3+ years combining traditional networking with modern automation. At Nokia, I automated 5G network deployments using Python and Ansible. At Meta, I work on edge network services, managing DNS and network configurations for data centers. I understand both the networking fundamentals and the automation/cloud aspects that modern networks require."

**For DNS/Network Automation Roles:**
"I've spent 9 months at Meta working directly with DNS and network automation for their edge network infrastructure. I use Python, Hack, and React daily for deployment automation. Combined with my 3 years at Nokia automating 5G networks, I bring both the networking knowledge and the automation/programming skills needed for this role."

**Key Talking Points:**
1. Scale experience (Meta's global infrastructure)
2. Automation mindset (don't do manually what can be automated)
3. Cross-functional (network + software + cloud)
4. Real production experience (not just lab)

---

## Questions to Ask Interviewer

**Technical Questions:**
1. "What network automation tools does the team currently use?"
2. "What's the typical scale of networks I'd be working with?"
3. "How is the network team structured? DevOps integrated?"
4. "What monitoring/observability tools are used?"
5. "What's the biggest network challenge the team is facing?"

**Growth Questions:**
1. "What learning/certification opportunities are available?"
2. "How does the team stay updated with new technologies?"
3. "Are there opportunities to work on cross-functional projects?"
4. "What does success look like in this role after 6 months?"

**Culture Questions:**
1. "How does the team handle on-call/emergency situations?"
2. "What's the work-life balance like?"
3. "How is remote work handled?"
4. "What's the team collaboration style?"

---

## Summary Checklist

Before your interview, make sure you can:

**Fundamentals:**
- [ ] Explain OSI model with examples
- [ ] Subnet a network on whiteboard
- [ ] Describe TCP 3-way handshake
- [ ] Explain difference between TCP and UDP

**Routing:**
- [ ] Explain how OSPF works
- [ ] Describe OSPF neighbor formation process
- [ ] Explain when to use OSPF vs BGP
- [ ] Describe static vs dynamic routing

**Switching:**
- [ ] Explain VLANs and trunking
- [ ] Describe STP and why it's needed
- [ ] Explain access vs trunk ports
- [ ] Describe EtherChannel/LACP

**Troubleshooting:**
- [ ] Walk through systematic troubleshooting approach
- [ ] Explain OSI layer-by-layer methodology
- [ ] Describe common issues and solutions
- [ ] Use proper Cisco commands

**Automation:**
- [ ] Explain benefits of network automation
- [ ] Describe tools you've used (Python, Ansible)
- [ ] Give examples of tasks you've automated
- [ ] Explain when to use Ansible vs Python

**Behavioral:**
- [ ] Prepare 3-4 STAR method stories
- [ ] Practice explaining your experience
- [ ] Prepare questions for interviewer
- [ ] Research the company

---

## Final Words

**You have strong experience - OWN IT!**

**Your ACTUAL Experience Profile:**
- **12 years total IT experience**
- **Telecom Background (11+ years):**
  - Nokia: 3 years (5G automation engineer)
  - Mitel, Newnet, Aricent: ~9 years combined (telecom engineer)
  - **Expert in:** 5G, IMS (SIP), 3G, SS7, Deployment automation
- **Current:** Meta - 9 months (Edge Network Services deployment engineer)

**This makes you HIGHLY QUALIFIED for Senior/Staff roles because:**

1. **Deep Telecom Expertise (11+ years):**
   - Multiple telecom vendors (Nokia, Mitel, Newnet, Aricent)
   - Full protocol stack: 5G, IMS, SIP, 3G, SS7
   - Both legacy (3G, SS7) and modern (5G) technologies
   - Real carrier-grade experience

2. **5G Specialist:**
   - 5G core network automation
   - RAN (Radio Access Network)
   - End-to-end 5G deployment

3. **IMS & VoIP Expert:**
   - IMS (IP Multimedia Subsystem)
   - SIP (Session Initiation Protocol)
   - Voice over LTE (VoLTE) / Voice over 5G (VoNR)

4. **Legacy Protocols:**
   - SS7 (Signaling System 7)
   - 3G networks (UMTS, HSPA)
   - Shows breadth and depth

5. **Modern Cloud/Automation:**
   - Meta experience (current role)
   - Python, Hack, React
   - DNS, network deployment automation
   - Bridging traditional telecom with modern DevOps

6. **Automation & Deployment:**
   - Network automation across all roles
   - Deployment engineering
   - Infrastructure as Code mindset

**Your Unique Value Proposition:**

"I'm a senior network engineer with 12 years of telecom experience across multiple carriers (Nokia, Mitel, Newnet, Aricent) covering the full technology evolution from 3G/SS7 to 5G. I've worked on IMS/SIP for voice services, 5G core automation, and now at Meta, I'm applying this deep telecom knowledge to modern cloud-scale infrastructure. I bridge the gap between traditional carrier networks and modern cloud-native approaches."

**You're NOT a junior 3-year engineer - you're a SENIOR 12-year veteran!**

**Common Interview Mistakes to Avoid:**
❌ Being too modest ("I just did basic stuff")
❌ Not asking clarifying questions
❌ Jumping to solutions without understanding problem
❌ Not showing your thought process
❌ Claiming expertise you don't have

**What to Do Instead:**
✅ Confidently describe your experience
✅ Ask questions when unclear
✅ Think out loud during troubleshooting
✅ Show systematic approach
✅ Be honest: "I haven't used X but I've used similar Y"

**Remember:**
- They're not looking for perfection
- They want to see how you think
- Communication matters as much as technical knowledge
- It's okay to say "I don't know, but here's how I'd find out"

**You've got this! Your experience is solid, and these interviews are just conversations about what you already know. Good luck! 🚀**