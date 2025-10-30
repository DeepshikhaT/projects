# 5G-Core-Automation Quick Start Guide

## 🚀 Get Started in 10 Minutes

This guide will help you understand and demo the project quickly.

---

## What Is This Project?

**Simple Answer:** This project shows how to automatically deploy and test a complete 5G network using modern cloud technologies.

**What it includes:**
- 5G Core Network (AMF, SMF, UPF, etc.)
- 5G Radio Access Network (gNB)
- Automated testing scripts
- Monitoring tools
- Complete documentation

---

## Understanding 5G in 2 Minutes

### What is 5G?

Think of 5G like this:
- **3G** = Dial-up internet (slow)
- **4G** = Broadband (fast)
- **5G** = Fiber optic speed on your phone (super fast!)

### Key Components

```
Your Phone → Cell Tower (gNB) → 5G Core Network → Internet
```

**5G Core Components:**
1. **AMF** - Checks who you are (like airport security)
2. **SMF** - Gives you internet access (like getting WiFi password)
3. **UPF** - Routes your data (like a smart mailman)

---

## Project Structure (Simplified)

```
5G-Core-Automation/
│
├── configuration/          # Settings for all 5G components
│   ├── 5g-core/           # Core network configs (AMF, SMF, UPF)
│   └── gnb/               # Cell tower config
│
├── testing/               # Automated test scripts
│   └── call_testing/      # Voice & data call tests
│
├── docker-compose.yml     # Run entire 5G network with one command!
│
├── README.md              # Complete documentation
├── INTERVIEW_GUIDE.md     # Everything you need for interviews
└── QUICKSTART.md          # This file!
```

---

## Quick Demo (No Installation Required)

### Step 1: Show the Architecture

Open `README.md` and scroll to the architecture diagram. Explain:

```
"This is a complete 5G network:
- Phone connects to gNB (cell tower)
- gNB connects to AMF (registration)
- SMF gives phone an IP address
- UPF routes data to internet"
```

### Step 2: Show Configuration Files

Open `configuration/5g-core/amf.yaml`:

```
"This is the AMF configuration. See all these comments? 
They explain what each setting does. This makes it easy 
to understand and maintain."
```

Key points to mention:
- MCC/MNC: Network identifier
- IP addresses: How components connect
- Security: Encryption settings

### Step 3: Show Testing Script

Open `testing/call_testing/voice_call_test.py`:

```
"This script automates voice call testing:
1. Registers two phones to network
2. Makes a call between them
3. Monitors quality (MOS score, latency)
4. Generates report"
```

Run through the code comments to show understanding.

### Step 4: Explain Automation

```
"Instead of manually configuring each component (which takes days):
- I define configuration once in code
- One command deploys everything
- Automated tests validate it works
- Can repeat 100 times, same result!"
```

---

## If You Want to Actually Run It

### Prerequisites

1. Install Docker Desktop
   - Download: https://www.docker.com/products/docker-desktop

2. That's it! (Docker Compose is included)

### Run the 5G Network

```bash
# Navigate to project folder
cd 5G-Core-Automation

# Start everything
docker-compose up -d

# Check status (should see all containers running)
docker-compose ps

# View logs
docker-compose logs -f amf

# Stop everything
docker-compose down
```

### What Just Happened?

When you ran `docker-compose up`:
1. Started MongoDB (subscriber database)
2. Started 5G Core components (AMF, SMF, UPF, etc.)
3. Started gNB (cell tower simulator)
4. Everything connected automatically!

---

## Interview Preparation (30 Minutes)

### 1. Read Interview Guide (15 min)

Open `INTERVIEW_GUIDE.md` and read these sections:
- "5G Basics - Start Here"
- "5G Network Components Explained Simply"
- "How a Phone Call Works in 5G"

**Focus on:**
- What each component does
- Simple analogies (hotel, restaurant, post office)
- Basic call flow

### 2. Practice Demo (10 min)

Practice this 2-minute pitch:

```
"I built a 5G network automation framework that:

1. Deploys complete 5G core network
   - All components (AMF, SMF, UPF, gNB)
   - Using Docker containers
   - Infrastructure as Code

2. Automates testing
   - Voice calls
   - Data sessions
   - Performance metrics

3. Includes monitoring
   - Real-time metrics
   - Quality dashboards

This shows I understand:
- 5G architecture and protocols
- Cloud and containerization
- Automation and testing
- DevOps practices"
```

### 3. Prepare for Questions (5 min)

Be ready to answer:

**Q: "What is 5G?"**
A: "5G is the fifth generation of mobile networks - much faster than 4G, with lower latency. Key features are higher speed, lower delay, and ability to connect many more devices."

**Q: "What components did you automate?"**
A: "I automated the complete 5G core network - AMF for registration, SMF for session management, UPF for data routing, plus the gNB (cell tower). All deployed as containers with one command."

**Q: "Have you worked with real 5G equipment?"**
A: "This is a demonstration project using open-source 5G implementations to show my understanding. The concepts apply to commercial equipment - it's about understanding the architecture and automation principles."

---

## Common Terms to Know

**IMSI** - Your phone's unique ID (like SSN for phones)

**AMF** - Access and Mobility Management (registration desk)

**SMF** - Session Management Function (gives you internet access)

**UPF** - User Plane Function (routes your data)

**gNB** - 5G base station (cell tower)

**PDU Session** - Data connection (like opening internet on phone)

**CU-DU Split** - Splitting cell tower into two parts for efficiency

**NFV** - Network Function Virtualization (running network as software)

---

## Troubleshooting

### Docker won't start
- Make sure Docker Desktop is running
- On Windows: Check if WSL2 is enabled
- Try: `docker-compose down` then `docker-compose up` again

### Containers keep restarting
- Check logs: `docker-compose logs [service-name]`
- Usually means configuration error
- Check configuration files in `configuration/` folder

### Need to reset everything
```bash
docker-compose down -v  # Stops and removes all data
docker-compose up -d    # Fresh start
```

---

## Next Steps

### To Learn More:

1. **Read Full Documentation**
   - `README.md` - Complete project details
   - `INTERVIEW_GUIDE.md` - In-depth explanations

2. **Explore Configuration Files**
   - Look at all YAML files in `configuration/`
   - Read the comments - they explain everything

3. **Study the Test Scripts**
   - `testing/call_testing/voice_call_test.py`
   - See how automated testing works

4. **Try Running It**
   - Follow "If You Want to Actually Run It" section above
   - Experiment with docker-compose commands

### To Prepare for Interviews:

1. **Understand the Architecture**
   - Draw it from memory
   - Explain what each component does

2. **Know the Automation Benefits**
   - Faster deployment
   - Consistent results
   - Reduced errors

3. **Practice Explaining**
   - Use simple analogies
   - Start high-level, then dive into details
   - Be ready to draw diagrams

---

## Success Checklist

Before your interview, make sure you can:

- [ ] Explain what 5G is in simple terms
- [ ] List the main 5G core components (AMF, SMF, UPF)
- [ ] Describe what each component does
- [ ] Explain the benefit of automation
- [ ] Walk through the project structure
- [ ] Demo the key files (configs, test scripts)
- [ ] Answer "Why did you build this?"
- [ ] Discuss technologies used (Docker, Python, Ansible)

---

## Final Tips

**Do's:**
✅ Use simple analogies (hotel, restaurant, post office)
✅ Draw diagrams to explain
✅ Show enthusiasm for 5G and automation
✅ Be honest about what's simulated vs. real
✅ Ask clarifying questions

**Don'ts:**
❌ Don't claim production experience if you don't have it
❌ Don't get lost in technical jargon
❌ Don't say "I just followed a tutorial"
❌ Don't be afraid to say "I don't know, but I can learn"

---

## Resources

**In This Project:**
- `README.md` - Complete documentation
- `INTERVIEW_GUIDE.md` - Interview preparation
- `docker-compose.yml` - See how components connect
- Configuration files - Learn 5G parameters

**External Learning:**
- 3GPP specs (official 5G standards)
- Open5GS documentation
- YouTube: 5G architecture videos

---

**You've got this! The project shows real skills - now show your understanding! 🚀📡**

---

## Quick Reference Card

**Project in One Sentence:**
"Automated deployment and testing framework for 5G core networks using containerization and Infrastructure as Code."

**Key Technologies:**
- 5G: Open5GS (AMF, SMF, UPF, gNB)
- Containers: Docker, Docker Compose
- Automation: Ansible, Python
- Cloud: AWS/Azure (Terraform)
- Monitoring: Kafka, Prometheus, Grafana

**What Makes It Special:**
- Complete end-to-end automation
- Real 5G protocols and flows
- Automated testing framework
- Production-ready practices
- Well-documented with learning focus

**Time Investment:**
- Quick review: 30 minutes
- Deep understanding: 2-3 hours
- Full mastery: 1-2 days

**ROI for Interviews:**
- Shows 5G knowledge: ✅
- Shows automation skills: ✅
- Shows cloud/DevOps: ✅
- Shows modern practices: ✅
- Differentiates you: ✅✅✅
