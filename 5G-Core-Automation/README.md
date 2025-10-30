# 5G-Core-Automation: 5G Network Function Virtualization & Orchestration

## 🚀 Project Overview

5G-Core-Automation is an end-to-end automation framework for deploying, configuring, and testing 5G core networks and Radio Access Networks (RAN). This project demonstrates expertise in 5G technologies, cloud infrastructure, network function virtualization (NFV), and telecom automation.

## 🎯 What This Project Demonstrates

This project showcases real-world 5G network engineering and automation skills:

- **5G Core Network Deployment:** Automated deployment of AMF, SMF, UPF, AUSF, UDM, NRF, PCF
- **gNB Configuration:** Automation of gNodeB (5G base station) setup with CU-DU split architecture
- **Cloud Infrastructure:** Infrastructure-as-Code for AWS/Azure deployment
- **Call Testing:** Automated voice and data call testing procedures
- **Network Monitoring:** Real-time monitoring using Kafka and custom dashboards
- **Packet Analysis:** Integration with Wireshark and QXDM for protocol analysis
- **NFV Orchestration:** Container-based network function deployment

## 🏗️ 5G Network Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     5G Core Network (5GC)                   │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐        │
│  │ AMF  │  │ SMF  │  │ UPF  │  │ AUSF │  │ UDM  │        │
│  │Access│  │Session│  │User  │  │Auth  │  │Data  │        │
│  │Mgmt  │  │Mgmt  │  │Plane │  │Server│  │Mgmt  │        │
│  └──┬───┘  └──┬───┘  └──┬───┘  └──────┘  └──────┘        │
└─────┼────────┼────────┼─────────────────────────────────────┘
      │        │        │
      │    N3  │    N6  │
      │        │        │
   N2 │     ┌──▼────────▼──┐
      │     │   Internet   │
      │     └──────────────┘
      │
┌─────▼─────────────────────────────────┐
│          5G RAN (gNodeB)              │
│  ┌────────────────┐                   │
│  │   gNB-CU-CP    │ (Control Plane)   │
│  │   Centralized  │                   │
│  │   Unit         │                   │
│  └───────┬────────┘                   │
│          │ F1-C                        │
│  ┌───────▼────────┐                   │
│  │   gNB-DU       │ (Data Unit)       │
│  │   Distributed  │                   │
│  │   Unit         │                   │
│  └───────┬────────┘                   │
└──────────┼────────────────────────────┘
           │
           │ 5G NR Radio
           │
    ┌──────▼──────┐
    │   UE (5G)   │ (User Equipment)
    │   Mobile    │
    └─────────────┘
```

### Key 5G Interfaces

- **N1:** UE ↔ AMF (NAS signaling)
- **N2:** gNB ↔ AMF (Control plane)
- **N3:** gNB ↔ UPF (User plane)
- **N4:** SMF ↔ UPF (Session management)
- **N6:** UPF ↔ Data Network (Internet)
- **F1-C:** gNB-CU ↔ gNB-DU (Control)
- **F1-U:** gNB-CU ↔ gNB-DU (User data)

## 📁 Project Structure

```
5G-Core-Automation/
│
├── infrastructure/
│   ├── terraform/
│   │   ├── aws/
│   │   │   ├── main.tf                 # AWS infrastructure
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   └── azure/
│   │       ├── main.tf                 # Azure infrastructure
│   │       └── variables.tf
│   └── ansible/
│       └── provision_servers.yml        # Server provisioning
│
├── deployment/
│   ├── docker-compose/
│   │   ├── 5g-core.yml                 # 5GC container deployment
│   │   └── gnb.yml                     # gNB container deployment
│   ├── kubernetes/
│   │   ├── core-network/
│   │   │   ├── amf-deployment.yaml
│   │   │   ├── smf-deployment.yaml
│   │   │   ├── upf-deployment.yaml
│   │   │   ├── ausf-deployment.yaml
│   │   │   └── udm-deployment.yaml
│   │   └── ran/
│   │       ├── gnb-cu-deployment.yaml
│   │       └── gnb-du-deployment.yaml
│   └── ansible/
│       ├── deploy_5g_core.yml          # Core network deployment
│       ├── deploy_gnb.yml              # gNB deployment
│       └── configure_cu_du.yml         # CU-DU split config
│
├── configuration/
│   ├── 5g-core/
│   │   ├── amf.yaml                    # AMF configuration
│   │   ├── smf.yaml                    # SMF configuration
│   │   ├── upf.yaml                    # UPF configuration
│   │   ├── ausf.yaml                   # AUSF configuration
│   │   └── udm.yaml                    # UDM configuration
│   ├── gnb/
│   │   ├── gnb_config.yaml             # gNB base configuration
│   │   ├── cu_config.yaml              # CU specific config
│   │   └── du_config.yaml              # DU specific config
│   └── templates/
│       ├── amf_template.j2
│       ├── gnb_template.j2
│       └── upf_template.j2
│
├── testing/
│   ├── call_testing/
│   │   ├── voice_call_test.py          # Voice call automation
│   │   ├── data_call_test.py           # Data call automation
│   │   └── ue_simulator.py             # UE simulator
│   ├── protocol_testing/
│   │   ├── nas_test.py                 # NAS protocol tests
│   │   ├── ngap_test.py                # NG-AP protocol tests
│   │   └── pfcp_test.py                # PFCP protocol tests
│   └── integration_tests/
│       ├── end_to_end_test.py
│       └── load_test.py
│
├── monitoring/
│   ├── kafka/
│   │   ├── kafka_producer.py           # Send telemetry to Kafka
│   │   ├── kafka_consumer.py           # Consume telemetry
│   │   └── kafka_config.yaml
│   ├── dashboards/
│   │   ├── grafana/
│   │   │   └── 5g-dashboard.json
│   │   └── kibana/
│   │       └── 5g-logs.json
│   └── scripts/
│       ├── network_monitor.py          # Real-time monitoring
│       ├── kpi_collector.py            # KPI collection
│       └── alert_manager.py            # Alerting
│
├── analysis/
│   ├── wireshark/
│   │   ├── capture_filter.txt          # Capture filters
│   │   └── display_filters.txt         # Display filters
│   ├── qxdm/
│   │   ├── qxdm_config.xml            # QXDM configuration
│   │   └── log_parser.py              # Parse QXDM logs
│   └── reports/
│       └── generate_report.py          # Test report generator
│
├── scripts/
│   ├── provisioning/
│   │   ├── create_subscribers.py       # Add subscribers to UDM
│   │   ├── configure_slices.py         # Network slicing
│   │   └── setup_qos.py               # QoS profiles
│   ├── automation/
│   │   ├── auto_deploy.sh             # Complete deployment script
│   │   ├── auto_test.sh               # Automated testing
│   │   └── health_check.py            # System health check
│   └── utilities/
│       ├── backup_configs.py
│       └── restore_configs.py
│
├── docs/
│   ├── 5G_ARCHITECTURE.md             # 5G architecture overview
│   ├── DEPLOYMENT_GUIDE.md            # Step-by-step deployment
│   ├── TESTING_PROCEDURES.md          # Testing methodologies
│   ├── TROUBLESHOOTING.md             # Common issues
│   └── NETWORK_TOPOLOGY.md            # Network diagrams
│
├── requirements.txt                    # Python dependencies
├── docker-compose.yml                  # Quick start deployment
└── README.md                          # This file
```

## 🛠️ Technology Stack

### Infrastructure & Orchestration
- **Terraform:** Infrastructure as Code (AWS/Azure)
- **Ansible:** Configuration management and deployment
- **Kubernetes:** Container orchestration
- **Docker:** Containerization
- **Helm:** Kubernetes package manager

### 5G Core Network Functions (Open5GS / Free5GC)
- **AMF (Access and Mobility Management Function)**
- **SMF (Session Management Function)**
- **UPF (User Plane Function)**
- **AUSF (Authentication Server Function)**
- **UDM (Unified Data Management)**
- **NRF (Network Repository Function)**
- **PCF (Policy Control Function)**
- **NSSF (Network Slice Selection Function)**

### RAN Components
- **gNB (gNodeB):** 5G base station
- **CU (Centralized Unit):** Control plane processing
- **DU (Distributed Unit):** PHY/MAC layer processing

### Monitoring & Analytics
- **Apache Kafka:** Real-time telemetry streaming
- **Prometheus:** Metrics collection
- **Grafana:** Visualization and dashboards
- **ELK Stack:** Log aggregation and analysis
- **Wireshark:** Packet capture and analysis
- **QXDM (Qualcomm eXtensible Diagnostic Monitor):** Log analysis

### Testing & Automation
- **Python 3.8+:** Automation scripts
- **pytest:** Test framework
- **Scapy:** Packet crafting and analysis
- **Robot Framework:** Test automation

### Cloud Providers
- **AWS:** EC2, VPC, EKS
- **Azure:** Virtual Machines, AKS

## 🚀 Quick Start

### Prerequisites

1. **Cloud Account:**
   - AWS account with EC2 access
   - OR Azure account with VM access

2. **Software Requirements:**
   ```bash
   # Install Terraform
   wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
   unzip terraform_1.5.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/

   # Install Ansible
   pip install ansible

   # Install kubectl (for Kubernetes)
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh

   # Install Python dependencies
   pip install -r requirements.txt
   ```

### Option 1: Quick Demo (Docker Compose)

```bash
# Clone repository
cd 5G-Core-Automation

# Start 5G Core + gNB
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f amf
docker-compose logs -f gnb
```

### Option 2: Cloud Deployment (AWS)

```bash
# Step 1: Deploy infrastructure
cd infrastructure/terraform/aws
terraform init
terraform plan
terraform apply

# Step 2: Deploy 5G Core Network
cd ../../../deployment/ansible
ansible-playbook deploy_5g_core.yml -i inventory/aws_hosts

# Step 3: Deploy gNB (CU + DU)
ansible-playbook deploy_gnb.yml -i inventory/aws_hosts

# Step 4: Verify deployment
python scripts/automation/health_check.py
```

### Option 3: Kubernetes Deployment

```bash
# Step 1: Create Kubernetes cluster (using EKS/AKS)
cd infrastructure/terraform/aws
terraform apply -target=module.eks

# Step 2: Deploy 5G Core to Kubernetes
cd ../../deployment/kubernetes
kubectl apply -f core-network/

# Step 3: Deploy gNB
kubectl apply -f ran/

# Step 4: Check pods
kubectl get pods -n 5g-core
kubectl get pods -n 5g-ran
```

## 📱 Call Testing

### Voice Call Test (Requires 2 UEs)

```bash
cd testing/call_testing

# Test voice call between two mobiles
python voice_call_test.py \
  --ue1 "IMSI-001010000000001" \
  --ue2 "IMSI-001010000000002" \
  --duration 60

# Output:
# [✓] UE1 registered to network
# [✓] UE2 registered to network
# [✓] Voice call initiated
# [✓] Call established
# [✓] Voice quality: MOS 4.2
# [✓] Call duration: 60 seconds
# [✓] Call terminated successfully
```

### Data Call Test (Requires 1 UE)

```bash
# Test data connectivity
python data_call_test.py \
  --ue "IMSI-001010000000001" \
  --test-type "ping" \
  --target "8.8.8.8"

# Output:
# [✓] UE registered to network
# [✓] PDU session established
# [✓] Data bearer active
# [✓] Ping test: 10ms latency
# [✓] Download speed: 100 Mbps
# [✓] Upload speed: 50 Mbps
```

### Automated End-to-End Test

```bash
# Run complete test suite
cd testing/integration_tests
python end_to_end_test.py

# Tests:
# 1. UE registration
# 2. PDU session establishment
# 3. Voice call (if 2 UEs available)
# 4. Data call
# 5. Handover testing
# 6. Service request
# 7. Deregistration
```

## 📊 Monitoring & Analysis

### Real-Time Monitoring with Kafka

```bash
# Start Kafka producer (collects telemetry from 5GC)
cd monitoring/kafka
python kafka_producer.py --topics "5g-core,gnb-metrics,call-records"

# Start consumer (process telemetry)
python kafka_consumer.py --topics "5g-core" --output dashboard

# View dashboard
# Open http://localhost:3000 (Grafana)
```

### Packet Analysis with Wireshark

```bash
# Capture N2 interface traffic (gNB ↔ AMF)
cd analysis/wireshark
tshark -i eth0 -f "sctp port 38412" -w n2_capture.pcap

# Analyze capture
wireshark n2_capture.pcap

# Apply display filter for specific procedures
# Filter: ngap.procedureCode == 21  (Initial UE Message)
# Filter: ngap.procedureCode == 14  (PDU Session Establishment)
```

### QXDM Log Analysis

```bash
# Parse QXDM logs
cd analysis/qxdm
python log_parser.py --input logs/qxdm_log.isf --output analysis/

# Generates:
# - nas_messages.csv (NAS signaling)
# - rrc_messages.csv (RRC signaling)
# - call_flow.pdf (Call flow diagram)
```

## 🏗️ 5G Core Components Explained

### AMF (Access and Mobility Management Function)

**Role:** Manages UE registration, mobility, and connection

**Key Functions:**
- Registration management (registration, deregistration)
- Connection management (CM-IDLE, CM-CONNECTED)
- Mobility management (handover, reselection)
- Authentication coordination

**Configuration:**
```yaml
# configuration/5g-core/amf.yaml
amf:
  ngap:
    - addr: 192.168.0.10
      port: 38412
  metrics:
    - addr: 0.0.0.0
      port: 9091
  guami:
    plmn_id:
      mcc: 001
      mnc: 01
    amf_id:
      region: 2
      set: 1
  tai:
    plmn_id:
      mcc: 001
      mnc: 01
    tac: 1
  plmn_support:
    - plmn_id:
        mcc: 001
        mnc: 01
      s_nssai:
        - sst: 1  # eMBB
```

### SMF (Session Management Function)

**Role:** Manages PDU sessions (data sessions)

**Key Functions:**
- Session establishment/modification/release
- IP address allocation
- QoS management
- Charging data collection

**Configuration:**
```yaml
# configuration/5g-core/smf.yaml
smf:
  sbi:
    - addr: 192.168.0.11
      port: 7777
  pfcp:
    - addr: 192.168.0.11
      port: 8805
  gtpu:
    - addr: 192.168.0.11
  subnet:
    - addr: 10.45.0.1/16  # UE IP pool
  dns:
    - 8.8.8.8
    - 8.8.4.4
  mtu: 1400
```

### UPF (User Plane Function)

**Role:** Routes and forwards user data packets

**Key Functions:**
- Packet routing and forwarding
- QoS enforcement
- Traffic usage reporting
- Lawful intercept

**Configuration:**
```yaml
# configuration/5g-core/upf.yaml
upf:
  pfcp:
    - addr: 192.168.0.12
      port: 8805
  gtpu:
    - addr: 192.168.0.12
      port: 2152
  subnet:
    - addr: 10.45.0.0/16
  dnn:
    - name: internet
      subnet: 10.45.0.0/16
```

### gNB (gNodeB) Configuration

**Role:** 5G base station (Radio Access Network)

**CU-DU Split Architecture:**
- **CU (Centralized Unit):** Handles higher layer protocols (PDCP, RRC)
- **DU (Distributed Unit):** Handles lower layers (PHY, MAC, RLC)

**Configuration:**
```yaml
# configuration/gnb/gnb_config.yaml
gnb:
  node_name: gNB-001
  mcc: 001
  mnc: 01
  tac: 1

  # N2 interface (to AMF)
  amf:
    addr: 192.168.0.10
    port: 38412

  # N3 interface (to UPF)
  upf:
    addr: 192.168.0.12
    port: 2152

  # Radio configuration
  cells:
    - cell_id: 1
      pci: 500  # Physical Cell ID
      dl_arfcn: 632628  # Downlink frequency
      bandwidth: 100  # MHz
      tx_power: 40  # dBm

  # CU-DU split
  cu:
    addr: 192.168.1.10
    f1_port: 2153
  du:
    addr: 192.168.1.20
    f1_port: 2153
```

## 🧪 Testing Procedures

### 1. Registration Test

**Purpose:** Verify UE can register to 5G network

```python
# testing/protocol_testing/nas_test.py
def test_registration():
    """Test UE registration procedure"""
    # 1. Power on UE
    ue = UESimulator(imsi="001010000000001")

    # 2. Send Registration Request
    response = ue.send_registration_request()

    # 3. Verify Authentication
    assert response.type == "AUTHENTICATION_REQUEST"
    ue.send_authentication_response()

    # 4. Verify Security Mode
    response = ue.receive_message()
    assert response.type == "SECURITY_MODE_COMMAND"
    ue.send_security_mode_complete()

    # 5. Verify Registration Accept
    response = ue.receive_message()
    assert response.type == "REGISTRATION_ACCEPT"
    assert response.registration_result == "5GS_REGISTRATION_SUCCESS"

    print("[✓] Registration successful")
```

### 2. PDU Session Establishment Test

**Purpose:** Verify data session can be established

```python
def test_pdu_session():
    """Test PDU session establishment"""
    ue = UESimulator(imsi="001010000000001")

    # Prerequisite: UE must be registered
    ue.register()

    # 1. Send PDU Session Establishment Request
    response = ue.send_pdu_session_request(dnn="internet")

    # 2. Verify PDU Session Establishment Accept
    assert response.type == "PDU_SESSION_ESTABLISHMENT_ACCEPT"
    assert response.pdu_session_id == 1
    assert response.ip_address is not None

    # 3. Verify connectivity
    ping_result = ue.ping("8.8.8.8")
    assert ping_result.success == True
    assert ping_result.latency < 50  # ms

    print(f"[✓] PDU Session established")
    print(f"[✓] UE IP: {response.ip_address}")
    print(f"[✓] Ping latency: {ping_result.latency}ms")
```

### 3. Voice Call Test

**Purpose:** Verify voice call between two UEs

```python
# testing/call_testing/voice_call_test.py
def test_voice_call(ue1_imsi, ue2_imsi, duration=60):
    """Test voice call between two UEs"""
    # Initialize UEs
    ue1 = UESimulator(imsi=ue1_imsi)
    ue2 = UESimulator(imsi=ue2_imsi)

    # Register both UEs
    ue1.register()
    ue2.register()

    # Establish PDU sessions
    ue1.establish_pdu_session()
    ue2.establish_pdu_session()

    # UE1 calls UE2
    call = ue1.initiate_voice_call(ue2.msisdn)

    # Verify call setup
    assert call.state == "ALERTING"

    # UE2 answers
    ue2.answer_call()
    assert call.state == "ACTIVE"

    # Monitor call quality
    for i in range(duration):
        time.sleep(1)
        metrics = call.get_metrics()

        assert metrics.mos > 3.5  # Mean Opinion Score
        assert metrics.packet_loss < 1  # %
        assert metrics.jitter < 30  # ms

    # Terminate call
    ue1.end_call()
    assert call.state == "TERMINATED"

    print(f"[✓] Voice call successful")
    print(f"[✓] Duration: {duration} seconds")
    print(f"[✓] Average MOS: {metrics.avg_mos}")
```

### 4. Data Call Test

**Purpose:** Verify data connectivity and throughput

```python
# testing/call_testing/data_call_test.py
def test_data_call(ue_imsi):
    """Test data connectivity and speed"""
    ue = UESimulator(imsi=ue_imsi)

    # Register and establish session
    ue.register()
    session = ue.establish_pdu_session(dnn="internet")

    # Test 1: Ping test
    ping_result = ue.ping("8.8.8.8", count=10)
    assert ping_result.success_rate > 95  # %
    assert ping_result.avg_latency < 50  # ms

    # Test 2: Download speed test
    download_result = ue.download_test(
        url="http://speedtest.example.com/100MB.bin",
        duration=10
    )
    assert download_result.speed > 10  # Mbps minimum

    # Test 3: Upload speed test
    upload_result = ue.upload_test(
        url="http://speedtest.example.com/upload",
        size="10MB"
    )
    assert upload_result.speed > 5  # Mbps minimum

    # Test 4: HTTP browsing test
    http_result = ue.http_get("https://www.google.com")
    assert http_result.status_code == 200
    assert http_result.load_time < 2  # seconds

    print(f"[✓] Data call successful")
    print(f"[✓] Ping: {ping_result.avg_latency}ms")
    print(f"[✓] Download: {download_result.speed} Mbps")
    print(f"[✓] Upload: {upload_result.speed} Mbps")
```

## 📈 Monitoring Dashboard

### Key Performance Indicators (KPIs)

```python
# monitoring/scripts/kpi_collector.py
class FiveGKPICollector:
    """Collect 5G network KPIs"""

    def collect_kpis(self):
        return {
            # Registration KPIs
            "registration_success_rate": self.get_registration_sr(),
            "registration_time": self.get_avg_registration_time(),

            # Session KPIs
            "pdu_session_success_rate": self.get_pdu_session_sr(),
            "pdu_session_setup_time": self.get_avg_pdu_setup_time(),

            # Call KPIs
            "call_success_rate": self.get_call_sr(),
            "call_setup_time": self.get_avg_call_setup_time(),
            "call_drop_rate": self.get_call_drop_rate(),

            # Data KPIs
            "average_throughput_dl": self.get_avg_throughput_dl(),
            "average_throughput_ul": self.get_avg_throughput_ul(),
            "average_latency": self.get_avg_latency(),

            # System KPIs
            "active_ues": self.get_active_ue_count(),
            "active_sessions": self.get_active_session_count(),
            "cpu_usage": self.get_cpu_usage(),
            "memory_usage": self.get_memory_usage()
        }
```

### Kafka Integration

```python
# monitoring/kafka/kafka_producer.py
from kafka import KafkaProducer
import json

class FiveGTelemetryProducer:
    """Send 5G telemetry to Kafka"""

    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_registration_event(self, ue_imsi, result):
        """Send registration event"""
        event = {
            "event_type": "REGISTRATION",
            "timestamp": datetime.now().isoformat(),
            "ue_imsi": ue_imsi,
            "result": result,
            "amf_id": "AMF-001",
            "tai": {"mcc": "001", "mnc": "01", "tac": 1}
        }
        self.producer.send('5g-events', value=event)

    def send_call_metrics(self, call_id, metrics):
        """Send call quality metrics"""
        data = {
            "call_id": call_id,
            "timestamp": datetime.now().isoformat(),
            "mos": metrics.mos,
            "packet_loss": metrics.packet_loss,
            "jitter": metrics.jitter,
            "latency": metrics.latency
        }
        self.producer.send('call-metrics', value=data)
```

## 🔧 Configuration Management

### Subscriber Management

```python
# scripts/provisioning/create_subscribers.py
def add_subscriber(imsi, msisdn, key, opc):
    """Add subscriber to UDM database"""
    subscriber = {
        "imsi": imsi,
        "msisdn": msisdn,
        "security": {
            "k": key,  # Permanent key
            "opc": opc,  # Operator code
            "amf": "8000",
            "sqn": "000000000000"
        },
        "subscription": {
            "default_slice": {
                "sst": 1,  # Slice type (1=eMBB)
                "sd": "010203"
            },
            "ambr": {
                "uplink": "1 Gbps",
                "downlink": "2 Gbps"
            }
        },
        "qos_profile": 9  # Default bearer
    }

    # Add to database
    udm_client.add_subscriber(subscriber)
    print(f"[✓] Added subscriber: {imsi}")
```

### Network Slicing

```python
# scripts/provisioning/configure_slices.py
def configure_network_slice(sst, sd, qos_profile):
    """Configure network slice"""
    slice_config = {
        "s_nssai": {
            "sst": sst,  # 1=eMBB, 2=URLLC, 3=mMTC
            "sd": sd
        },
        "qos": {
            "5qi": qos_profile,
            "priority": 1,
            "packet_delay_budget": 100,  # ms
            "packet_error_rate": 1e-6
        },
        "resources": {
            "max_ues": 1000,
            "max_sessions": 5000,
            "bandwidth": {
                "uplink": "                 "uplink": "500 Mbps",
                "uplink": "                "downlink": "1 Gbps"
                "uplink": "            }
                "uplink": "        }
                "uplink": "    }

                "uplink": "    # Configure on AMF/SMF
                "uplink": "    amf_client.configure_slice(slice_config)
                "uplink": "    smf_client.configure_slice(slice_config)
                "uplink": "    print(f"[✓] Configured slice: SST={sst}, SD={sd}")
                "uplink": "```

                "uplink": "## 🎯 Real-World Use Cases

                "uplink": "### Use Case 1: Deploy Complete 5G Network

                "uplink": "**Scenario:** Set up a complete 5G core network and RAN in AWS

                "uplink": "```bash
                "uplink": "# Full deployment script
                "uplink": "./scripts/automation/auto_deploy.sh --cloud aws --region us-east-1

                "uplink": "# What it does:
                "uplink": "# 1. Creates VPC, subnets, security groups (Terraform)
                "uplink": "# 2. Launches EC2 instances for 5GC components
                "uplink": "# 3. Deploys containers (AMF, SMF, UPF, etc.)
                "uplink": "# 4. Deploys gNB-CU and gNB-DU
                "uplink": "# 5. Configures all components
                "uplink": "# 6. Validates deployment with health checks
                "uplink": "# 7. Adds sample subscribers
                "uplink": "```

                "uplink": "### Use Case 2: Automated Call Testing

                "uplink": "**Scenario:** Test voice calls after network deployment

                "uplink": "```bash
                "uplink": "# Automated test suite
                "uplink": "./scripts/automation/auto_test.sh --type voice --ues 10

                "uplink": "# Output:
                "uplink": "# Test Results:
                "uplink": "# - UE Registration: 10/10 successful (100%)
                "uplink": "# - PDU Sessions: 10/10 established (100%)
                "uplink": "# - Voice Calls: 10/10 successful (100%)
                "uplink": "# - Average Call Setup Time: 2.3s
                "uplink": "# - Average MOS: 4.1
                "uplink": "# - Call Drop Rate: 0%
                "uplink": "```

                "uplink": "### Use Case 3: Real-Time Monitoring

                "uplink": "**Scenario:** Monitor live 5G network performance

                "uplink": "```bash
                "uplink": "# Start monitoring
                "uplink": "python monitoring/scripts/network_monitor.py --realtime

                "uplink": "# Dashboard shows:
                "uplink": "# - Active UEs: 245
                "uplink": "# - Active Sessions: 312
                "uplink": "# - Call Success Rate: 99.2%
                "uplink": "# - Average Latency: 15ms
                "uplink": "# - Throughput (DL/UL): 1.2 Gbps / 600 Mbps
                "uplink": "# - System Health: ✓ All components operational
                "uplink": "```

                "uplink": "## 📚 Skills Demonstrated

                "uplink": "### 5G/Telecom Expertise
                "uplink": "- ✅ 5G core network architecture (AMF, SMF, UPF, AUSF, UDM)
                "uplink": "- ✅ 5G RAN architecture (gNB, CU-DU split)
                "uplink": "- ✅ 5G protocols (NAS, NGAP, PFCP, GTP-U)
                "uplink": "- ✅ Network slicing concepts
                "uplink": "- ✅ QoS and traffic management
                "uplink": "- ✅ Subscriber management
                "uplink": "- ✅ Call flows (registration, session establishment, voice/data)

                "uplink": "### Cloud & Infrastructure
                "uplink": "- ✅ Infrastructure as Code (Terraform)
                "uplink": "- ✅ Cloud deployment (AWS, Azure)
                "uplink": "- ✅ Container orchestration (Kubernetes, Docker)
                "uplink": "- ✅ Network function virtualization (NFV)
                "uplink": "- ✅ Microservices architecture

                "uplink": "### Automation & Scripting
                "uplink": "- ✅ Ansible for configuration management
                "uplink": "- ✅ Python for automation and testing
                "uplink": "- ✅ CI/CD concepts
                "uplink": "- ✅ Test automation frameworks
                "uplink": "- ✅ Infrastructure orchestration

                "uplink": "### Monitoring & Analytics
                "uplink": "- ✅ Real-time telemetry (Kafka)
                "uplink": "- ✅ Metrics collection (Prometheus)
                "uplink": "- ✅ Visualization (Grafana)
                "uplink": "- ✅ Log aggregation (ELK)
                "uplink": "- ✅ Packet analysis (Wireshark, QXDM)

                "uplink": "### Testing & Validation
                "uplink": "- ✅ Protocol testing (NAS, NGAP, PFCP)
                "uplink": "- ✅ Call testing (voice and data)
                "uplink": "- ✅ Performance testing
                "uplink": "- ✅ Integration testing
                "uplink": "- ✅ End-to-end testing

                "uplink": "## 🔍 Packet Analysis Guide

                "uplink": "### Wireshark Filters

                "uplink": "```bash
                "uplink": "# N2 Interface (gNB ↔ AMF) - NGAP
                "uplink": "ngap

                "uplink": "# Registration procedure
                "uplink": "ngap.procedureCode == 21  # Initial UE Message
                "uplink": "ngap.procedureCode == 15  # Downlink NAS Transport

                "uplink": "# PDU Session Establishment
                "uplink": "ngap.procedureCode == 29  # PDU Session Resource Setup Request

                "uplink": "# N3 Interface (gNB ↔ UPF) - GTP-U
                "uplink": "gtp

                "uplink": "# N4 Interface (SMF ↔ UPF) - PFCP
                "uplink": "pfcp

                "uplink": "# Filter by IMSI
                "uplink": "nas_5gs.mm.imsi == "001010000000001"
                "uplink": "```

                "uplink": "### QXDM Configuration

                "uplink": "```xml
                "uplink": "<!-- analysis/qxdm/qxdm_config.xml -->
                "uplink": "<QXDMConfiguration>
                "uplink": "  <LogItems>
                "uplink": "    <Item>NAS 5G Messages</Item>
                "uplink": "    <Item>RRC Messages</Item>
                "uplink": "    <Item>PDCP Messages</Item>
                "uplink": "    <Item>MAC Messages</Item>
                "uplink": "    <Item>PHY Messages</Item>
                "uplink": "  </LogItems>
                "uplink": "  <Filters>
                "uplink": "    <Filter name="Registration">
                "uplink": "      <Include>Registration Request</Include>
                "uplink": "      <Include>Registration Accept</Include>
                "uplink": "      <Include>Authentication Request</Include>
                "uplink": "    </Filter>
                "uplink": "    <Filter name="Session">
                "uplink": "      <Include>PDU Session Establishment Request</Include>
                "uplink": "      <Include>PDU Session Establishment Accept</Include>
                "uplink": "    </Filter>
                "uplink": "  </Filters>
                "uplink": "</QXDMConfiguration>
                "uplink": "```

                "uplink": "## 📖 Documentation

                "uplink": "### Additional Resources

                "uplink": "- **[5G_ARCHITECTURE.md](docs/5G_ARCHITECTURE.md)** - Detailed 5G architecture explanation
                "uplink": "- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Step-by-step deployment instructions
                "uplink": "- **[TESTING_PROCEDURES.md](docs/TESTING_PROCEDURES.md)** - Complete testing methodologies
                "uplink": "- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions
                "uplink": "- **[NETWORK_TOPOLOGY.md](docs/NETWORK_TOPOLOGY.md)** - Network diagrams and topology

                "uplink": "## 🚧 Known Limitations

                "uplink": "- **UE Simulator:** Uses simulated UEs, not real devices (for demo purposes)
                "uplink": "- **Radio:** Does not include actual RF components (focuses on core/control plane)
                "uplink": "- **Scale:** Optimized for lab environment, not carrier-grade deployment
                "uplink": "- **Features:** Implements core features, some advanced 5G features not included

                "uplink": "## 🔮 Future Enhancements

                "uplink": "- [ ] Integration with real 5G modems/devices
                "uplink": "- [ ] Support for SA (Standalone) and NSA (Non-Standalone) modes
                "uplink": "- [ ] Advanced network slicing with dynamic resource allocation
                "uplink": "- [ ] AI/ML for network optimization
                "uplink": "- [ ] Integration with MEC (Multi-Access Edge Computing)
                "uplink": "- [ ] Support for voice over 5G (VoNR)
                "uplink": "- [ ] Roaming scenarios (visited/home network)
                "uplink": "- [ ] Network analytics and predictive maintenance

                "uplink": "## 👤 Author

                "uplink": "**Deepshikha Tripathi**

                "uplink": "This project demonstrates:
                "uplink": "- 5G/Telecom engineering expertise
                "uplink": "- Cloud infrastructure and NFV skills
                "uplink": "- Network automation proficiency
                "uplink": "- Testing and validation experience
                "uplink": "- Real-world problem-solving ability

                "uplink": "## 📄 License

                "uplink": "This is a portfolio/demonstration project.

                "uplink": "## 🤝 Contributing

                "uplink": "This is a personal portfolio project, but feedback and suggestions are welcome!

                "uplink": "---

                "uplink": "## Quick Command Reference

                "uplink": "### Deployment
                "uplink": "```bash
                "uplink": "# Deploy everything
                "uplink": "./scripts/automation/auto_deploy.sh

                "uplink": "# Deploy only 5G core
                "uplink": "ansible-playbook deployment/ansible/deploy_5g_core.yml

                "uplink": "# Deploy only gNB
                "uplink": "ansible-playbook deployment/ansible/deploy_gnb.yml
                "uplink": "```

                "uplink": "### Testing
                "uplink": "```bash
                "uplink": "# Voice call test
                "uplink": "python testing/call_testing/voice_call_test.py --ue1 IMSI1 --ue2 IMSI2

                "uplink": "# Data call test
                "uplink": "python testing/call_testing/data_call_test.py --ue IMSI1

                "uplink": "# Full test suite
                "uplink": "python testing/integration_tests/end_to_end_test.py
                "uplink": "```

                "uplink": "### Monitoring
                "uplink": "```bash
                "uplink": "# Start monitoring
                "uplink": "python monitoring/scripts/network_monitor.py

                "uplink": "# Start Kafka producer
                "uplink": "python monitoring/kafka/kafka_producer.py

                "uplink": "# View Grafana dashboard
                "uplink": "# http://localhost:3000
                "uplink": "```

                "uplink": "### Management
                "uplink": "```bash
                "uplink": "# Add subscriber
                "uplink": "python scripts/provisioning/create_subscribers.py --imsi 001010000000001

                "uplink": "# Health check
                "uplink": "python scripts/automation/health_check.py

                "uplink": "# Backup configs
                "uplink": "python scripts/utilities/backup_configs.py
                "uplink": "```

                "uplink": "---

                "uplink": "**Note:** This project demonstrates 5G concepts using open-source implementations (Open5GS/Free5GC). For production deployment, consider licensed commercial 5G core solutions.

                "uplink": "## 🎓 Learning Resources

                "uplink": "### 3GPP Specifications
                "uplink": "- TS 23.501: System architecture for 5G
                "uplink": "- TS 23.502: Procedures for 5G system
                "uplink": "- TS 38.300: NR overall description
                "uplink": "- TS 38.401: NG-RAN architecture

                "uplink": "### Recommended Reading
                "uplink": "- 5G System Design by Patrick Marsch
                "uplink": "- 5G NR: Architecture, Technology, Implementation by Dongfeng Yuan
                "uplink": "- Introduction to 5G Mobile Communications by Juha Korhonen

                "uplink": "**Ready to showcase your 5G and cloud automation skills! 🚀**
