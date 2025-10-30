# 5G-Core-Automation - Complete Interview Guide for Beginners

## 📚 Table of Contents
1. [5G Basics - Start Here!](#5g-basics---start-here)
2. [5G Network Components Explained Simply](#5g-network-components-explained-simply)
3. [How a Phone Call Works in 5G](#how-a-phone-call-works-in-5g)
4. [Automation & Cloud Concepts](#automation--cloud-concepts)
5. [Interview Questions & Answers](#interview-questions--answers)
6. [How to Demo This Project](#how-to-demo-this-project)
7. [Troubleshooting Scenarios](#troubleshooting-scenarios)
8. [Terms You Must Know](#terms-you-must-know)

---

## 5G Basics - Start Here!

### What is 5G? (Explain like I'm 5 years old)

**You:** "What is 5G?"

**Answer:** "5G is like 4G, but faster and smarter. Think of it like this:

- **3G** = Like a bicycle (slow, basic calling/texting)
- **4G/LTE** = Like a car (fast enough for video calls, streaming)
- **5G** = Like a jet plane (super fast, can do things 4G can't)

**What makes 5G special:**
1. **Faster:** Download a movie in 10 seconds (not 10 minutes)
2. **Low Delay:** When you click, things happen instantly (good for gaming, self-driving cars)
3. **More Connections:** Can connect millions of devices (smart homes, factories)

### How is 5G Different from 4G?

| Feature | 4G/LTE | 5G |
|---------|--------|-----|
| **Speed** | 100 Mbps | 1-10 Gbps (10-100x faster!) |
| **Latency** | 50ms | 1-10ms (5x better response) |
| **Architecture** | Monolithic (all in one box) | Modular (split into pieces) |
| **Deployment** | Hardware boxes | Software/Cloud (Virtual) |
| **Network Slicing** | No | Yes (different virtual networks) |

**Real World Example:**
- **4G:** You're watching Netflix, video buffers sometimes
- **5G:** You're watching 4K Netflix, downloading files, on video call - NO buffering!

---

## 5G Network Components Explained Simply

### Think of 5G Network like a Restaurant

```
Your Phone = Customer
gNB (Cell Tower) = Waiter
5G Core = Kitchen/Management

Customer → Waiter → Kitchen → Food comes back → Waiter → Customer
Phone    → gNB   → 5G Core → Data comes back → gNB   → Phone
```

### The 5G Core Network - The "Brain"

The 5G core has several components. Think of them like departments in a company:

#### 1. AMF (Access and Mobility Management Function)

**Simple Explanation:**
"AMF is like the reception desk at a hotel"

**What it does:**
- Checks your ID when you arrive (authentication)
- Remembers your room number (tracking)
- Knows where you are (mobility management)

**Real-World Example:**
```
You turn on your phone:
1. Phone: "Hi, I'm here! My ID is [IMSI]"
2. AMF: "Let me check... Yes, you're a valid customer"
3. AMF: "You're now registered. You can use the network!"
```

**Interview Question:** "What is AMF?"
**Answer:** "AMF is the first point of contact when a phone connects to 5G. It handles registration, authentication, and tracks where phones are located in the network."

#### 2. SMF (Session Management Function)

**Simple Explanation:**
"SMF is like a hotel concierge who sets up services for you"

**What it does:**
- Gives you an IP address (like your room number)
- Sets up your internet connection (PDU Session)
- Manages your data session quality

**Real-World Example:**
```
You want to browse internet:
1. You: "I want to use internet"
2. SMF: "OK, your IP address is 10.45.1.100"
3. SMF tells UPF: "Route data for IP 10.45.1.100 to this phone"
4. Now you can browse!
```

**Interview Question:** "What is SMF?"
**Answer:** "SMF manages data sessions. When you want to use internet on your phone, SMF creates a PDU Session, assigns you an IP address, and tells the network how to route your data."

#### 3. UPF (User Plane Function)

**Simple Explanation:**
"UPF is like the highway for your data packets"

**What it does:**
- Routes data packets between your phone and internet
- Like a post office - receives packages, delivers to destination
- Can prioritize important traffic (video calls over web browsing)

**Real-World Example:**
```
You visit google.com:

Phone → gNB → UPF → Internet → Google
  ↑                              ↓
  └──────← UPF ←─────────────────┘

UPF knows:
- "10.45.1.100 is that phone over there"
- "Route web traffic this way"
- "Route video calls that way (priority)"
```

**Interview Question:** "What is UPF?"
**Answer:** "UPF handles the actual user data. It's like a smart router that knows which phone gets which data packets. It routes traffic between phones and the internet, and can prioritize important traffic."

#### 4. UDM (Unified Data Management)

**Simple Explanation:**
"UDM is like the customer database"

**What it does:**
- Stores subscriber information (your phone number, plan, etc.)
- Stores authentication keys (your password)
- Stores what services you're allowed to use

**Real-World Example:**
```
AMF asks UDM:
AMF: "Is IMSI 001010000000001 a valid subscriber?"
UDM: "Yes! Here's their info:
      - Phone number: +1-555-1234
      - Plan: Unlimited data
      - Authentication key: [encrypted]"
```

#### 5. AUSF (Authentication Server Function)

**Simple Explanation:**
"AUSF is like a security guard checking IDs"

**What it does:**
- Verifies you are who you say you are
- Checks your password (authentication key)
- Prevents unauthorized access

**Real-World Example:**
```
Phone trying to connect:
1. Phone: "I'm subscriber X"
2. AUSF: "Prove it - solve this math problem" [challenge]
3. Phone: "Here's the answer" [using secret key]
4. AUSF: "Correct! You're authentic!"
```

### The RAN (Radio Access Network) - The "Connection"

#### gNB (gNodeB) - The Cell Tower

**Simple Explanation:**
"gNB is the cell tower that your phone talks to via radio waves"

**What it does:**
- Broadcasts 5G signal
- Receives data from your phone
- Forwards it to the 5G core network

**Modern Innovation: CU-DU Split**

Old way: Entire gNB in one big box at the tower
New way: Split into two parts:

```
gNB-CU (Centralized Unit) → In cloud/data center (the "brain")
   │
   │ Connected via fiber
   │
gNB-DU (Distributed Unit) → At cell tower (the "muscle")
```

**Why split?**
1. **Cost:** DU at tower is cheaper, CU can be in cloud
2. **Flexibility:** One CU can serve many DUs
3. **Maintenance:** Update CU software centrally, not at each tower

**Interview Question:** "What is CU-DU split?"
**Answer:** "CU-DU split divides the gNB into two parts. The DU (Distributed Unit) handles time-critical radio functions at the cell tower. The CU (Centralized Unit) handles higher-level protocols and can be placed in a data center or cloud. This saves cost and makes the network more flexible."

---

## How a Phone Call Works in 5G

### Complete Step-by-Step Flow

**Scenario:** You want to call your friend

```
[You]         [gNB]      [AMF]    [SMF]    [UPF]    [Internet]
  │             │          │         │         │          │
  │ 1. Turn on phone       │         │         │          │
  ├────────────>│          │         │         │          │
  │             │          │         │         │          │
  │ 2. Search for network  │         │         │          │
  │             │ (broadcasts sync signals)    │          │
  │<────────────┤          │         │         │          │
  │             │          │         │         │          │
  │ 3. Connect to gNB      │         │         │          │
  ├────────────>│          │         │         │          │
  │             │          │         │         │          │
  │ 4. Registration Request│         │         │          │
  ├────────────>├─────────>│         │         │          │
  │             │          │ 5. Auth check      │          │
  │             │          │<───>(UDM/AUSF)     │          │
  │             │ 6. Accept│         │         │          │
  │<────────────┤<─────────┤         │         │          │
  │             │          │         │         │          │
  │ 7. Want internet!      │         │         │          │
  ├────────────>├─────────>├────────>│         │          │
  │             │          │         │ 8. Give IP         │
  │             │          │         │ 9. Setup route     │
  │             │          │         ├────────>│          │
  │             │ 10. IP assigned    │         │          │
  │<────────────┤<─────────┤<────────┤         │          │
  │             │          │         │         │          │
  │ 11. Browse web         │         │         │          │
  ├────────────>├──────────┼─────────┼────────>├─────────>│
  │             │          │         │         │          │
  │             │          │         │         │ 12. Response
  │<────────────┤<─────────┼─────────┼─────────┤<─────────┤
```

### Detailed Explanation of Each Step

**Step 1-2: Finding the Network**
```
Your phone scans frequencies looking for 5G signals
gNB broadcasts "sync signals" every 20ms
Phone finds signal and reads network info (MCC, MNC, TAC)
Phone: "Found network 001-01!"
```

**Step 3: Initial Connection (RRC)**
```
Phone: "I want to connect" (RRC Setup Request)
gNB: "OK, you're connected" (RRC Setup Complete)
Now phone has a radio connection to gNB
```

**Step 4-6: Registration (NAS)**
```
Phone: "I want to register. My IMSI is 001010000000001"
gNB forwards to AMF
AMF: "Let me check with UDM if this is a valid subscriber"
UDM: "Yes, valid!"
AMF: "Authenticate yourself" (Challenge)
Phone: "Here's my response" (Proof of identity)
AMF: "Verified! Registration accepted"
```

**Step 7-10: Getting Internet (PDU Session)**
```
Phone: "I want to use internet!"
AMF forwards request to SMF
SMF: "OK, I'll set this up"
SMF picks IP from pool: 10.45.1.100
SMF tells UPF: "Route traffic for 10.45.1.100 via gNB"
SMF tells phone: "Your IP is 10.45.1.100"
Phone: "Great! Now I can browse!"
```

**Step 11-12: Using Data**
```
You type: www.google.com

Phone → gNB → UPF → Internet → Google servers
  ↑                                    ↓
  └──← gNB ←── UPF ←── Internet ←──────┘

You see Google homepage!
```

---

## Automation & Cloud Concepts

### What is Network Function Virtualization (NFV)?

**Old Way (Physical Network)**
```
[Big expensive box] = AMF
[Big expensive box] = SMF
[Big expensive box] = UPF

Problems:
- Very expensive ($100,000+ per box)
- Hard to upgrade (need to swap hardware)
- Takes space (racks and racks of equipment)
- Takes power (electricity bills)
```

**New Way (Virtualized Network)**
```
[One server / Cloud]
  ├─ Container: AMF
  ├─ Container: SMF
  ├─ Container: UPF
  └─ Container: UDM

Benefits:
- Much cheaper (software on commodity hardware)
- Easy to upgrade (just update Docker container)
- Flexible (can run in cloud, on-premise, at edge)
- Scalable (need more capacity? Add more containers)
```

**Interview Question:** "What is NFV?"
**Answer:** "NFV means running network functions as software instead of dedicated hardware. Instead of buying expensive proprietary boxes, we run network functions (like AMF, SMF) as containers or VMs on standard servers or in the cloud. This is cheaper, more flexible, and easier to maintain."

### What is Infrastructure as Code (IaC)?

**Traditional Way:**
```
1. Login to AWS console
2. Click "Create EC2 instance"
3. Select size, network, storage
4. Click create
5. Wait...
6. Repeat 100 times for 100 servers!
```

**IaC Way (using Terraform):**
```hcl
# File: main.tf
resource "aws_instance" "5g_core" {
  count = 100                    # Create 100 instances!
  ami = "ami-12345"
  instance_type = "t3.xlarge"
}

# Run: terraform apply
# Creates all 100 servers in 5 minutes!
```

**Benefits:**
- **Repeatable:** Same code creates same infrastructure every time
- **Version Control:** Track changes in Git
- **Fast:** Create 100 servers in minutes, not days
- **Documented:** Code IS the documentation

**Interview Question:** "What is Infrastructure as Code?"
**Answer:** "IaC means defining infrastructure (servers, networks, etc.) using code instead of manual clicking. Tools like Terraform let me write a configuration file that describes what I want, then automatically creates it. This is faster, repeatable, and version-controlled."

### What is Docker/Containers?

**Think of containers like shipping containers:**

Old Way (shipping):
- Different types of cargo need different ships
- Trucks, trains, ships - all different
- Lots of handling, slow, expensive

New Way (shipping containers):
- Standard container fits anywhere
- Ship, train, truck - same container
- Fast, efficient, cheap

**Same concept for software:**

Old Way:
```
App needs:
- Specific OS version
- Specific library versions
- Specific configuration

Deploy on Server A: Works!
Deploy on Server B: Breaks! (different OS)
```

New Way (Docker):
```
[Container]
  ├─ App
  ├─ All dependencies
  ├─ Configuration
  └─ Runs anywhere!

Deploy anywhere: Always works!
```

**Interview Question:** "Why use Docker for 5G?"
**Answer:** "Docker containers package the 5G network function (like AMF) with all its dependencies. This means I can deploy the same container on my laptop, on AWS, on Azure - it works the same everywhere. It's portable, consistent, and easy to manage."

---

## Interview Questions & Answers

### Basic Questions

**Q1: "Explain 5G to a non-technical person."**

**Answer:**
"5G is the fifth generation of mobile networks - it's like the internet connection for your phone, but much faster and more capable than 4G.

Imagine:
- **4G** is like a 2-lane highway
- **5G** is like a 10-lane superhighway

With 5G you can:
- Download a movie in seconds instead of minutes
- Have video calls with no lag
- Connect smart devices (cars, fridges, watches) seamlessly
- Use new technologies like VR/AR smoothly

The big difference is not just speed, but also how it's built - 5G uses software and cloud technology, making it more flexible and cost-effective."

**Q2: "What are the main components of 5G core network?"**

**Answer:**
"The 5G core has several main components:

1. **AMF (Access & Mobility Mgmt)** - Handles phone registration and mobility
2. **SMF (Session Mgmt)** - Manages data sessions and assigns IP addresses
3. **UPF (User Plane)** - Routes actual user data (like a smart router)
4. **UDM (Data Mgmt)** - Stores subscriber information
5. **AUSF (Authentication)** - Verifies user identity

Think of them like departments in a company:
- AMF = Reception
- SMF = Resource Manager
- UPF = Delivery Department
- UDM = Database/HR
- AUSF = Security

They work together to connect your phone and get you online."

**Q3: "What is the difference between 4G and 5G architecture?"**

**Answer:**

**4G Architecture:**
- Monolithic (EPC = one big system)
- Hardware-based
- Limited flexibility
- Components: MME, SGW, PGW, HSS

**5G Architecture:**
- Modular (Service-Based Architecture)
- Software/Cloud-based (NFV)
- Highly flexible
- Components: AMF, SMF, UPF, UDM, etc.

**Key Differences:**
1. **Interfaces:** 4G uses point-to-point, 5G uses service-based (APIs)
2. **Deployment:** 4G needs hardware boxes, 5G can run in cloud
3. **Scalability:** 5G scales better (add containers)
4. **Network Slicing:** 5G supports multiple virtual networks

**Simple Analogy:**
- 4G = Traditional phone with physical buttons
- 5G = Smartphone with apps you can add/remove"

**Q4: "What is network slicing?"**

**Answer:**
"Network slicing is like having multiple virtual networks on the same physical infrastructure.

**Analogy: Highway Lanes**
```
Same physical highway, but different lanes for:
- Lane 1: Ambulances (emergency - high priority)
- Lane 2: Buses (public transport - medium priority)
- Lane 3-5: Regular cars (normal priority)
```

**5G Network Slices:**
```
Same 5G network, but different slices for:
- Slice 1: Emergency services (ultra-low latency)
- Slice 2: Video streaming (high bandwidth)
- Slice 3: IoT devices (low power, many connections)
```

**Real Example:**
- Your phone streaming Netflix uses Slice 1 (high bandwidth)
- Self-driving car uses Slice 2 (ultra-low latency)
- Smart home sensors use Slice 3 (low power)

All on the same 5G network, but with different performance guarantees!"

### Technical Questions

**Q5: "Explain the registration process in 5G."**

**Answer:**
"When you turn on your 5G phone, here's what happens:

**Step 1: Network Discovery**
- Phone scans for 5G signals
- Finds gNB broadcasting sync signals
- Reads network identity (MCC, MNC, TAC)

**Step 2: RRC Connection**
- Phone: 'I want to connect' (RRC Setup Request)
- gNB: 'OK' (RRC Setup Response)
- Radio connection established

**Step 3: Registration Request**
- Phone → gNB → AMF: 'I want to register. My IMSI is X'
- Message: NAS Registration Request

**Step 4: Authentication**
- AMF queries UDM: 'Is IMSI X valid?'
- UDM: 'Yes, here's the auth key'
- AMF challenges phone with crypto puzzle
- Phone solves it using secret key
- AMF: 'Authenticated!'

**Step 5: Security Setup**
- AMF: 'Use this encryption' (Security Mode Command)
- Phone: 'OK' (Security Mode Complete)
- All future messages encrypted

**Step 6: Registration Accept**
- AMF: 'Registration successful!'
- Phone now registered and can use network

**Time:** Typically 2-3 seconds"

**Q6: "What is PDU Session and how is it established?"**

**Answer:**
"PDU Session is a data session - it's what you need to use internet on your phone.

**PDU = Protocol Data Unit (fancy name for 'data session')**

**Why do we need it?**
- You need an IP address to browse internet
- You need a 'tunnel' from your phone to internet
- You need QoS (quality) settings

**Establishment Process:**

1. **Phone Request**
```
Phone: 'I want internet!'
Sends: PDU Session Establishment Request
To: AMF
```

2. **SMF Gets Involved**
```
AMF: 'OK, let me ask SMF to set this up'
AMF → SMF: 'Create session for this phone'
```

3. **SMF Does Magic**
```
SMF:
- Picks IP from pool → 10.45.1.100
- Chooses QoS profile → Default (9)
- Selects UPF → UPF-1
```

4. **UPF Configuration**
```
SMF → UPF: 'Route traffic for 10.45.1.100 via gNB'
UPF: 'OK, configured!'
```

5. **Tell the Phone**
```
SMF → AMF → gNB → Phone: 'Session established!'
   Your IP: 10.45.1.100
   DNS: 8.8.8.8
```

6. **Done!**
```
Phone can now browse internet!
```

**Components Involved:**
- Phone (requester)
- gNB (forwarder)
- AMF (orchestrator)
- SMF (session manager)
- UPF (data router)

**Time:** Typically < 1 second"

**Q7: "Explain CU-DU split in gNB."**

**Answer:**
"CU-DU split divides the gNB (cell tower) into two parts:

**Traditional gNB (Old Way):**
```
[gNB - One Big Box at Tower]
  - RRC (signaling)
  - PDCP (security)
  - RLC (error correction)
  - MAC (scheduling)
  - PHY (radio)

Problems:
- Expensive hardware at every tower
- Hard to upgrade
- Can't leverage cloud
```

**CU-DU Split (New Way):**
```
gNB-CU (Centralized Unit) - In Data Center/Cloud
  - RRC (signaling)
  - PDCP (security)
  - Can be virtualized
  - Serves multiple DUs

    ↕ F1 Interface (fiber connection)

gNB-DU (Distributed Unit) - At Cell Tower
  - RLC (error correction)
  - MAC (scheduling)
  - PHY (radio)
  - Smaller, cheaper hardware
```

**Benefits:**

1. **Cost Savings**
   - DU hardware is cheaper
   - One CU serves many DUs
   - Example: 1 CU serves 50 DUs

2. **Flexibility**
   - CU can be in cloud (AWS, Azure)
   - CU can be at edge (near towers)
   - Easy to move

3. **Maintenance**
   - Update CU software centrally
   - Don't need to visit each tower
   - Saves time and money

4. **Scalability**
   - Need more capacity? Add DUs
   - CU scales horizontally (add more CU instances)

**Real Example:**
```
Verizon 5G:
- 10,000 cell towers (DUs)
- 200 regional data centers (CUs)
- Each CU serves ~50 DUs
- Software upgrade: Update 200 CUs (not 10,000 towers!)
```

**F1 Interface:**
- Connects CU ↔ DU
- Uses fiber optic cable
- Carries control + user data"

### Automation Questions

**Q8: "Why automate 5G deployment?"**

**Answer:**
"Automation is essential for 5G because:

**1. Complexity**
- 5G has many components (AMF, SMF, UPF, gNB, etc.)
- Manual configuration is error-prone
- One typo can break the network

**2. Scale**
- Operators deploy thousands of sites
- Manual: Takes months, costs millions
- Automated: Takes days, costs thousands

**3. Consistency**
- Manual: Each engineer does things differently
- Automated: Same code = same result everywhere

**4. Speed**
- Manual deployment: 1-2 days per site
- Automated deployment: 10-15 minutes per site

**5. Testing**
- Manual testing: Takes hours, prone to mistakes
- Automated testing: Runs in minutes, repeatable

**Real Example:**
```
Deploy 5G core in 100 locations:

Manual:
- 2 days per site × 100 sites = 200 days
- 2 engineers × $500/day = $200,000
- Risk of mistakes: HIGH

Automated (My Project):
- 15 minutes per site × 100 sites = 25 hours
- 1 engineer × $500/day × 2 days = $1,000
- Risk of mistakes: LOW
- ROI: Saved $199,000!
```"

**Q9: "Explain your automation workflow."**

**Answer:**
"My automation workflow has multiple stages:

**Stage 1: Infrastructure (Terraform)**
```bash
terraform apply
# Creates:
# - Cloud VMs (AWS/Azure)
# - Networks and subnets
# - Security groups
# - Load balancers
```

**Stage 2: Provisioning (Ansible)**
```bash
ansible-playbook provision_servers.yml
# Installs:
# - Docker
# - Kubernetes
# - Required libraries
# - Security patches
```

**Stage 3: Deployment (Ansible/K8s)**
```bash
ansible-playbook deploy_5g_core.yml
# Deploys:
# - AMF containers
# - SMF containers
# - UPF containers
# - All with proper configs
```

**Stage 4: Configuration**
```bash
# Applies configurations from templates
# Sets up:
# - Network interfaces
# - Routing
# - Security
```

**Stage 5: Testing**
```bash
python testing/integration_tests/end_to_end_test.py
# Runs:
# - Registration tests
# - Session establishment tests
# - Call tests
# - Performance tests
```

**Stage 6: Monitoring**
```bash
# Starts monitoring:
# - Kafka producers/consumers
# - Prometheus metrics
# - Grafana dashboards
```

**Total Time:** 30-45 minutes for complete deployment!"

---

## How to Demo This Project

### 30-Second Elevator Pitch

"I built a complete 5G network automation framework that deploys and tests 5G core networks and radio access networks. Instead of manually configuring network functions which takes days and is error-prone, my automation deploys a complete 5G network in under an hour using Infrastructure-as-Code and containerization. The project includes automated testing scripts that validate voice calls, data sessions, and network performance, and integrates with monitoring tools like Kafka and Grafana for real-time visibility."

### 5-Minute Demo Script

**Minute 1: Show Architecture Diagram**
```
"Let me show you the 5G architecture I automated.

[Draw or show diagram]

Here's the 5G core network - AMF handles registration, SMF manages sessions, UPF routes data. The gNB is the cell tower using CU-DU split architecture. All these components are deployed as containers."
```

**Minute 2: Show Configuration Files**
```
"Here's my AMF configuration. Notice the detailed comments explaining each parameter. This file is a template - Ansible fills in the actual values during deployment.

[Open amf.yaml]

See these IP addresses and ports? These are all automated - no manual configuration needed."
```

**Minute 3: Show Automation Script**
```
"Let me show you the deployment automation.

[Open deploy_5g_core.yml playbook]

This Ansible playbook:
1. Deploys all 5G components
2. Configures them
3. Starts services
4. Validates deployment

One command deploys the entire network:
ansible-playbook deploy_5g_core.yml
```

**Minute 4: Show Testing**
```
"Once deployed, I run automated tests.

[Open voice_call_test.py]

This script:
- Simulates two 5G phones
- Registers them to the network
- Makes a voice call
- Monitors quality (MOS, latency, jitter)
- Generates report

[Show sample output if available]

Real networks use actual devices, but for demo I simulate the behavior."
```

**Minute 5: Show Monitoring**
```
"Finally, monitoring.

[Show monitoring architecture]

- Kafka streams telemetry data
- Prometheus collects metrics
- Grafana visualizes dashboards
- Can see real-time KPIs

This shows I understand not just deployment, but ongoing operations too."
```

### Questions You'll Get

**Q: "Have you worked with real 5G equipment?"**

**Honest Answer:**
"This is a demonstration project using open-source 5G implementations (Open5GS/Free5GC) to show my understanding of 5G architecture and automation skills. In a production environment, I would work with commercial 5G core vendors like Ericsson, Nokia, or Samsung, but the concepts are the same - it's about automating deployment, testing, and monitoring regardless of the vendor."

**Q: "How is this different from manual deployment?"**

**Answer:**
"Manual deployment involves:
- SSH'ing into each server
- Editing configuration files by hand
- Starting services manually
- High risk of typos and inconsistencies

My automated approach:
- Define configuration once in version control
- Run one command to deploy
- Consistent results every time
- Can deploy 10 sites or 100 sites with same effort
- All changes are tracked in Git"

**Q: "What cloud platforms does this support?"**

**Answer:**
"I've designed it to be cloud-agnostic using:
- Terraform for infrastructure (supports AWS, Azure, GCP)
- Docker containers (run anywhere)
- Kubernetes for orchestration (EKS, AKS, GKE)

I have Terraform templates for both AWS and Azure. The same 5G containers run on both platforms - that's the beauty of containerization."

---

## Troubleshooting Scenarios

### Scenario 1: UE Can't Register

**Interviewer:** "A phone can't register to the 5G network. How do you troubleshoot?"

**Your Answer (Step by Step):**

```
1. CHECK: Is phone receiving signal?
   Command: Check gNB logs
   Look for: "RRC Setup Request received"

2. CHECK: Is gNB connected to AMF?
   Command: kubectl logs amf-pod | grep "NG Setup"
   Look for: "NG Setup successful with gNB"

3. CHECK: Is IMSI valid in UDM?
   Command: Query UDM database
   Look for: Subscriber entry exists

4. CHECK: Authentication working?
   Command: Check AMF logs during registration
   Look for: "Authentication successful" or auth failures

5. CHECK: Network configuration matches?
   Verify:
   - MCC/MNC in gNB matches AMF
   - TAC in gNB matches AMF
   - Allowed slices match

6. CHECK: Message flow
   Use: Wireshark on N2 interface
   Filter: ngap
   Look for: InitialUEMessage, RegistrationRequest

Common Issues:
- IMSI not in UDM database → Add subscriber
- Wrong authentication key → Update UDM
- gNB not connected to AMF → Check N2 interface config
- MCC/MNC mismatch → Fix gNB or AMF config
```

### Scenario 2: No Data Connection

**Interviewer:** "Phone is registered but can't browse internet. Troubleshoot."

**Your Answer:**

```
1. CHECK: PDU Session established?
   Command: Check SMF logs
   Look for: "PDU Session Establishment Accept"

2. CHECK: IP address assigned?
   Expected: Phone should have IP from pool (10.45.x.x)
   Command: Check SMF logs for IP allocation

3. CHECK: UPF routing configured?
   Command: Check UPF logs
   Look for: "Session created for IP 10.45.x.x"

4. CHECK: Data path
   Test: Can UPF ping 8.8.8.8?
   Test: Can UPF ping phone IP?

5. CHECK: N3 tunnel
   Command: tcpdump on N3 interface
   Look for: GTP-U packets flowing

6. CHECK: DNS working?
   Test: From phone, can resolve www.google.com?
   Expected: DNS should be 8.8.8.8 (from SMF)

Common Issues:
- SMF can't reach UPF → Check N4 interface
- No IP addresses in pool → Increase subnet size
- UPF not routing → Check NAT/routing rules
- Firewall blocking → Check security groups
```

### Scenario 3: Poor Call Quality

**Interviewer:** "Voice calls work but quality is poor. How do you diagnose?"

**Your Answer:**

```
1. MEASURE: Get metrics
   - MOS score (should be > 4.0)
   - Packet loss (should be < 1%)
   - Jitter (should be < 30ms)
   - Latency (should be < 50ms)

2. CHECK: Network conditions
   Command: Monitor UPF metrics
   Look for:
   - High CPU/memory usage
   - Interface errors
   - Packet drops

3. CHECK: QoS settings
   Verify: Voice traffic has proper priority (5QI=1)
   Command: Check SMF QoS configuration

4. CHECK: Radio conditions
   Command: Check gNB radio metrics
   Look for:
   - Signal strength (RSRP)
   - Interference (SINR)
   - Throughput

5. ANALYZE: Packet capture
   Tool: Wireshark
   Filter: rtp (Real-time Transport Protocol)
   Look for:
   - Out of order packets
   - Duplicate packets
   - Packet loss patterns

6. TEST: Different scenarios
   - Different locations
   - Different times of day
   - Different UEs

Common Issues:
- Network congestion → Add capacity
- Wrong QoS profile → Fix SMF config
- Poor radio conditions → Adjust gNB power/frequency
- Codec issues → Check IMS settings
```

---

## Terms You Must Know

### Basic Terms

**IMSI** (International Mobile Subscriber Identity)
- Your phone's unique ID (like SSN for phones)
- Example: 001010000000001
- Stored in SIM card

**MSISDN** (Mobile Station International Subscriber Directory Number)
- Your phone number
- Example: +1-555-123-4567

**MCC** (Mobile Country Code)
- Identifies country
- Example: 310 = USA, 001 = Test

**MNC** (Mobile Network Code)
- Identifies operator within country
- Example: 001 = Test operator

**PLMN** (Public Land Mobile Network)
- MCC + MNC = identifies a specific network
- Example: 310-410 = AT&T in USA

**TAC** (Tracking Area Code)
- Identifies a "zone" in the network
- Phone registers to a tracking area
- Example: TAC=1

**DNN** (Data Network Name)
- Name of data network (like "internet" or "ims")
- Used in PDU Session

**5QI** (5G QoS Identifier)
- Quality of service level (1-9)
- 1 = Highest priority (voice)
- 9 = Default (web browsing)

### Protocol Terms

**NAS** (Non-Access Stratum)
- Messages between phone and AMF
- Examples: Registration Request, PDU Session Request

**NGAP** (NG Application Protocol)
- Messages between gNB and AMF (N2 interface)
- Examples: Initial UE Message, PDU Session Resource Setup

**PFCP** (Packet Forwarding Control Protocol)
- Messages between SMF and UPF (N4 interface)
- SMF tells UPF how to route packets

**GTP-U** (GPRS Tunneling Protocol - User plane)
- Tunnels user data between gNB and UPF (N3 interface)
- Wraps IP packets for transport

**RRC** (Radio Resource Control)
- Messages between phone and gNB
- Manages radio connection

### Architecture Terms

**SBA** (Service Based Architecture)
- 5G architecture style
- Components communicate via APIs/services
- Flexible and modular

**NFV** (Network Function Virtualization)
- Running network functions as software
- Instead of dedicated hardware boxes

**CU** (Centralized Unit)
- Part of gNB (the "brain")
- Can be in cloud/data center

**DU** (Distributed Unit)
- Part of gNB (the "muscle")
- At cell tower site

**PDU Session** (Protocol Data Unit Session)
- Data session/connection
- Like opening an internet connection on your phone

**Network Slice**
- Virtual network on shared infrastructure
- Different slices for different services

---

## Final Preparation Checklist

### Before Interview

- [ ] Can explain 5G in simple terms to non-technical person
- [ ] Can draw 5G architecture from memory
- [ ] Can explain what each component does (AMF, SMF, UPF, gNB)
- [ ] Can describe registration flow step-by-step
- [ ] Can describe PDU session establishment
- [ ] Can explain CU-DU split and why it's used
- [ ] Can explain NFV and its benefits
- [ ] Can explain why automation is important
- [ ] Can demo the project (even if simulated)
- [ ] Can troubleshoot common issues

### During Interview

- [ ] Start with high-level explanation
- [ ] Use simple analogies (hotel, restaurant, highway)
- [ ] Draw diagrams to explain concepts
- [ ] Be honest about simulation vs. real equipment
- [ ] Show enthusiasm for 5G and automation
- [ ] Ask clarifying questions
- [ ] Relate to real-world use cases

### Key Messages to Convey

✅ "I understand 5G architecture end-to-end"
✅ "I can automate complex deployments"
✅ "I know both networking AND cloud/automation"
✅ "I can test and validate deployments"
✅ "I understand operations, not just deployment"
✅ "I'm ready to work with real 5G equipment and learn vendor-specific details"

---

## Summary

### What You've Built

1. **Complete 5G Network Automation**
   - Infrastructure as Code (Terraform)
   - Configuration management (Ansible)
   - Container orchestration (Docker/K8s)

2. **Testing Framework**
   - Automated call testing
   - Protocol testing
   - Performance testing

3. **Monitoring & Operations**
   - Real-time telemetry (Kafka)
   - Metrics collection (Prometheus)
   - Visualization (Grafana)

### Skills Demonstrated

**5G/Telecom:**
- 5G architecture and protocols
- Network function configuration
- Call flows and procedures
- Quality monitoring

**Cloud/DevOps:**
- Infrastructure as Code
- Container orchestration
- CI/CD concepts
- Configuration management

**Programming:**
- Python automation
- YAML configurations
- Bash scripting

**Testing:**
- Test automation
- Integration testing
- Performance testing

### What Makes You Special

"I'm not just a 5G engineer who understands protocols, and I'm not just a DevOps engineer who can deploy containers. I'm someone who bridges both worlds - I understand the telecom side (5G, protocols, call flows) AND the cloud side (automation, containers, IaC). This combination is rare and valuable in today's 5G deployments where everything is moving to cloud and automation."

**Good luck with your interviews! You've built something impressive - now show them your knowledge! 🚀📡**
