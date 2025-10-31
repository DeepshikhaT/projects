# Monitoring Tools Crash Course - What You ACTUALLY Need

## 🎯 Reality Check: Do You Need ALL These Tools?

### The Truth About Job Requirements

**When a job says:** "Experience with Prometheus, Grafana, ELK, Kafka, Datadog, Splunk..."

**What they ACTUALLY mean:** "You should know monitoring/observability concepts and be familiar with 1-2 tools"

**You DON'T need to master all tools!**

---

## 📊 Monitoring Tools - Priority Matrix

### Tier 1: MUST KNOW (Learn Hands-On)
**Pick ONE monitoring stack:**

**Option A: Prometheus + Grafana** ⭐ RECOMMENDED
- **Why:** Most popular in DevOps/Cloud
- **Time to learn:** 2-3 days
- **Job mentions:** 70%+
- **Best for:** Metrics, infrastructure monitoring
- **Learn this!**

**Option B: ELK Stack** (Elasticsearch + Logstash + Kibana)
- **Why:** Popular for log management
- **Time to learn:** 3-4 days
- **Job mentions:** 60%+
- **Best for:** Logs, security, search
- **Learn if:** Targeting security/log analysis roles

### Tier 2: AWARENESS LEVEL (Know What They Do)

**Kafka**
- **What it is:** Message streaming platform
- **Learn level:** Understand concepts, maybe run basic example
- **Time:** 4-6 hours
- **Job mentions:** 40%+
- **When needed:** Backend/data engineering roles

**Datadog / New Relic / AppDynamics**
- **What they are:** Commercial monitoring SaaS
- **Learn level:** Watch videos, know features
- **Time:** 2-3 hours
- **Reality:** Companies train you on these

**CloudWatch (AWS)**
- **What it is:** AWS native monitoring
- **Learn level:** Basic usage when learning AWS
- **Time:** Included in AWS learning

### Tier 3: JUST KNOW THEY EXIST

- Splunk (expensive enterprise tool)
- Dynatrace (APM tool)
- Nagios/Zabbix (older monitoring)

---

## 🚀 2-DAY PROMETHEUS + GRAFANA CRASH COURSE

**Goal:** Get hands-on experience you can discuss in interviews

### Day 1: Prometheus (4-5 hours)

#### Morning (2-3 hours): Theory + Setup

**What is Prometheus?**
```
Prometheus = Metrics collection and storage system

Think of it like:
- A database that stores time-series metrics
- Pulls metrics from your applications periodically
- Stores: "At 10:00 AM, CPU was 45%"
- You query it: "Show me CPU for last 24 hours"
```

**Key Concepts (15 minutes reading):**
1. **Metrics:** Numbers you track (CPU, memory, requests)
2. **Scraping:** Prometheus pulls metrics from targets
3. **Time Series:** Data points over time
4. **PromQL:** Query language (like SQL for metrics)
5. **Exporters:** Programs that expose metrics

**Setup (30 minutes hands-on):**

```bash
# Option 1: Docker (Easiest)
docker run -d -p 9090:9090 prom/prometheus

# Access: http://localhost:9090

# Option 2: Docker Compose (Better)
# Create docker-compose.yml
```

```yaml
# docker-compose.yml
version: '3'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
```

```yaml
# prometheus.yml (configuration)
global:
  scrape_interval: 15s  # How often to collect metrics

scrape_configs:
  # Monitor Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

```bash
# Start
docker-compose up -d

# Check
docker-compose ps
curl http://localhost:9090
```

**Explore UI (30 minutes):**
1. Open http://localhost:9090
2. Try queries in "Graph" tab:
   - `up` (shows which targets are up)
   - `prometheus_http_requests_total` (total requests)
   - `rate(prometheus_http_requests_total[5m])` (requests per second)
3. Click "Status" → "Targets" (see what's monitored)

#### Afternoon (2 hours): Monitor Something Real

**Monitor Your Computer (Node Exporter)**

```bash
# Add to docker-compose.yml
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
```

```yaml
# Update prometheus.yml - add this job
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

```bash
# Restart
docker-compose down
docker-compose up -d

# Wait 15 seconds for scrape
# Check: http://localhost:9090/targets
# Should see "node" job
```

**Try Queries:**
```promql
# CPU usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk usage
(node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100
```

**Add Your Python App (Advanced - 1 hour)**

```python
# Install: pip install prometheus-client
from prometheus_client import start_http_server, Counter, Gauge
import time
import psutil

# Create metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests')
CPU_USAGE = Gauge('app_cpu_percent', 'CPU usage percent')

def monitor():
    # Expose metrics on port 8000
    start_http_server(8000)
    
    while True:
        # Update metrics
        CPU_USAGE.set(psutil.cpu_percent())
        time.sleep(15)

if __name__ == '__main__':
    monitor()
```

Add to prometheus.yml:
```yaml
  - job_name: 'myapp'
    static_configs:
      - targets: ['host.docker.internal:8000']  # Your app
```

**Day 1 Complete! You now:**
✅ Understand Prometheus basics
✅ Have it running in Docker
✅ Can write PromQL queries
✅ Monitor system metrics
✅ Can add monitoring to Python apps

---

### Day 2: Grafana (4-5 hours)

#### Morning (2-3 hours): Setup + First Dashboard

**What is Grafana?**
```
Grafana = Visualization tool for metrics

Think of it like:
- Prometheus stores data (database)
- Grafana displays data (dashboards)
- Like Excel charts for your metrics
```

**Setup (15 minutes):**

```yaml
# Add to docker-compose.yml
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

```bash
# Restart
docker-compose down
docker-compose up -d

# Access: http://localhost:3000
# Login: admin / admin (change password when prompted)
```

**Connect Prometheus (10 minutes):**
1. Click "⚙️ Configuration" (left sidebar) → "Data Sources"
2. Click "Add data source"
3. Select "Prometheus"
4. URL: `http://prometheus:9090`
5. Click "Save & Test" (should see "Data source is working")

**Create First Dashboard (30 minutes):**
1. Click "+" → "Dashboard" → "Add new panel"
2. In query box, enter: `up`
3. Panel title: "Service Status"
4. Click "Apply"
5. Click "Save dashboard" (top right) → Name: "System Monitoring"

**More Panels (1-2 hours - practice!):**

**Panel 2: CPU Usage**
```promql
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```
- Visualization: Time series (graph)
- Unit: Percent (0-100)
- Title: "CPU Usage"

**Panel 3: Memory Usage**
```promql
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100
```
- Visualization: Gauge
- Unit: Percent (0-100)
- Title: "Memory Usage"

**Panel 4: Disk Space**
```promql
100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)
```
- Visualization: Gauge
- Unit: Percent (0-100)
- Thresholds: Green (0-80), Yellow (80-90), Red (90-100)
- Title: "Disk Usage"

**Panel 5: Network Traffic**
```promql
rate(node_network_receive_bytes_total[5m])
```
- Visualization: Time series
- Unit: Bytes/sec
- Title: "Network In"

#### Afternoon (2 hours): Import Ready-Made Dashboard

**Use Community Dashboards (Smart Way!):**
1. Go to https://grafana.com/grafana/dashboards/
2. Search "Node Exporter Full"
3. Find dashboard #1860 (popular!)
4. Copy the ID: 1860

**Import:**
1. In Grafana: "+" → "Import"
2. Paste ID: 1860
3. Click "Load"
4. Select Prometheus data source
5. Click "Import"

**Boom! Professional dashboard in 2 minutes!**

**Explore Features (1 hour):**
- Variables (dropdown filters)
- Time ranges (last 1h, 24h, 7d)
- Refresh intervals (auto-update)
- Panel inspector (see queries)
- Export dashboard (JSON)

**Create Alert (30 minutes):**
1. Edit a panel (CPU usage)
2. Click "Alert" tab
3. "Create Alert"
4. Condition: `WHEN avg() OF query(A, 5m, now) IS ABOVE 80`
5. Save

**Day 2 Complete! You now:**
✅ Have Grafana running
✅ Connected to Prometheus
✅ Created custom dashboards
✅ Imported professional dashboards
✅ Understand alerting basics

---

## 🎨 Add Monitoring to Your Existing Projects

### Project 1: EdgeNet-Demo (Backend Flask App)

**Add Prometheus Metrics (10 minutes):**

```python
# backend/app.py
from prometheus_client import Counter, Histogram, generate_latest
from flask import Response
import time

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')

# Middleware
@app.before_request
def before_request():
    request._prometheus_start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(request, '_prometheus_start_time'):
        duration = time.time() - request._prometheus_start_time
        REQUEST_DURATION.observe(duration)
        REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint).inc()
    return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

**Update docker-compose.yml:**
```yaml
services:
  backend:
    # ... existing config
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=5000"
      - "prometheus.path=/metrics"
```

**Update Prometheus config:**
```yaml
  - job_name: 'edgenet-demo'
    static_configs:
      - targets: ['backend:5000']
```

**Dashboard Queries:**
```promql
# Request rate
rate(app_requests_total[5m])

# Average response time
rate(app_request_duration_seconds_sum[5m]) / rate(app_request_duration_seconds_count[5m])

# Error rate (add error counter)
rate(app_errors_total[5m])
```

---

### Project 2: 5G-Core-Automation (Already has metrics!)

**Your docker-compose.yml can include:**
```yaml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

# Scrape metrics from AMF, SMF, UPF
```

**5G-Specific Metrics to Monitor:**
```promql
# Registration success rate
rate(amf_registrations_success_total[5m]) / rate(amf_registrations_total[5m]) * 100

# PDU session setup time
histogram_quantile(0.95, rate(smf_pdu_session_setup_duration_seconds_bucket[5m]))

# UPF throughput
rate(upf_packets_transmitted_total[5m])

# Active UEs
amf_active_ues
```

---

### Project 3: NetOps-Automation (Network Monitoring)

**Python Script with Metrics:**

```python
# scripts/network_monitor_with_metrics.py
from prometheus_client import Gauge, start_http_server
import netmiko
import time

# Metrics
DEVICE_UP = Gauge('network_device_up', 'Device reachable', ['device'])
DEVICE_CPU = Gauge('network_device_cpu_percent', 'CPU usage', ['device'])
DEVICE_MEMORY = Gauge('network_device_memory_percent', 'Memory usage', ['device'])
INTERFACE_STATUS = Gauge('network_interface_up', 'Interface status', ['device', 'interface'])

def monitor_device(device):
    try:
        connection = netmiko.ConnectHandler(**device)
        
        # Device is up
        DEVICE_UP.labels(device=device['host']).set(1)
        
        # Get CPU
        cpu = connection.send_command('show processes cpu | include CPU')
        cpu_percent = parse_cpu(cpu)
        DEVICE_CPU.labels(device=device['host']).set(cpu_percent)
        
        # Get interfaces
        interfaces = connection.send_command('show ip interface brief', use_textfsm=True)
        for iface in interfaces:
            status = 1 if iface['status'].lower() == 'up' else 0
            INTERFACE_STATUS.labels(
                device=device['host'],
                interface=iface['interface']
            ).set(status)
        
        connection.disconnect()
    except:
        DEVICE_UP.labels(device=device['host']).set(0)

if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics
    
    devices = [...]  # Your device list
    
    while True:
        for device in devices:
            monitor_device(device)
        time.sleep(60)  # Check every minute
```

---

## 📸 Take Screenshots for Resume!

**What to Capture:**

1. **Prometheus Targets Page**
   - Shows all monitored services
   - Screenshot: http://localhost:9090/targets

2. **Grafana Dashboard**
   - Your custom dashboard with multiple panels
   - Shows real metrics
   - Screenshot: http://localhost:3000

3. **Alert Example**
   - Alert configuration
   - Shows you understand alerting

**Add to Resume/LinkedIn:**
- "Implemented Prometheus + Grafana monitoring for Python applications"
- "Created custom Grafana dashboards for 5G core network KPIs"
- "Automated network device monitoring with Prometheus exporters"

---

## 🎤 Interview Talking Points

### When Asked: "Do you have monitoring experience?"

**Answer:**
"Yes, I've worked with Prometheus and Grafana for application and infrastructure monitoring. 

For example, in my EdgeNet-Demo project, I instrumented the Python backend with Prometheus client library to track request rates, response times, and error rates. I created Grafana dashboards to visualize these metrics with alerting for critical thresholds.

I also have experience with network device monitoring, where I collect metrics from routers and switches using custom exporters and display them in Grafana. I understand the importance of observability in production systems and how to use metrics to troubleshoot issues quickly."

### Common Questions:

**Q: "What's the difference between metrics, logs, and traces?"**
**A:**
- **Metrics:** Numbers over time (CPU 45%, requests/sec: 100) - Prometheus
- **Logs:** Text events ("User X logged in at 10:00 AM") - ELK
- **Traces:** Request path through services (microservices debugging) - Jaeger/Zipkin

**Q: "How do you choose what to monitor?"**
**A:** "I follow the Four Golden Signals:
1. **Latency:** How long requests take
2. **Traffic:** How many requests
3. **Errors:** How many fail
4. **Saturation:** How full resources are (CPU, memory, disk)

Plus application-specific metrics like user registrations, 5G session success rate, etc."

**Q: "Have you set up alerts?"**
**A:** "Yes, I configure alerts for:
- High error rates (> 5%)
- Slow response times (> 2 seconds)
- Resource saturation (CPU > 80%, Disk > 90%)
- Service unavailability

Alerts go to Slack/PagerDuty depending on severity."

---

## 🎓 Quick Learning: Kafka (If Needed)

**If a job mentions Kafka, here's 4-hour crash course:**

### What is Kafka?
```
Kafka = Distributed message streaming platform

Think of it like:
- A super-fast messaging queue
- Producers send messages to topics
- Consumers read messages from topics
- Messages are persisted (not lost)
```

**Use Cases:**
- Real-time data pipelines
- Event streaming
- Log aggregation
- Microservices communication

**Quick Setup (Docker):**
```yaml
# docker-compose.yml
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
```

**Python Example:**
```python
from kafka import KafkaProducer, KafkaConsumer

# Producer (send messages)
producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('my-topic', b'Hello Kafka!')

# Consumer (receive messages)
consumer = KafkaConsumer('my-topic', bootstrap_servers='localhost:9092')
for message in consumer:
    print(message.value)
```

**Interview Answer:**
"I understand Kafka as a distributed streaming platform. I've used it for real-time telemetry collection in my 5G automation project, where network events are published to Kafka topics and consumed by monitoring applications. I know it's used for building data pipelines and event-driven architectures."

---

## ✅ 2-Day Challenge Checklist

### Day 1: Prometheus
- [ ] Install Prometheus with Docker
- [ ] Add Node Exporter
- [ ] Write 5 PromQL queries
- [ ] Add metrics to one Python app
- [ ] Take screenshot of targets page

### Day 2: Grafana
- [ ] Install Grafana
- [ ] Connect to Prometheus
- [ ] Create custom dashboard (4+ panels)
- [ ] Import community dashboard
- [ ] Create one alert
- [ ] Take screenshot of dashboard

### Bonus (If time):
- [ ] Add monitoring to EdgeNet-Demo
- [ ] Create 5G-specific metrics
- [ ] Write blog post about it (LinkedIn)
- [ ] Update resume with "Prometheus + Grafana"

---

## 🎯 Final Reality Check

**What Interviewers ACTUALLY Expect:**

✅ "I've used Prometheus and Grafana to monitor applications"
✅ "I understand metrics collection and visualization"
✅ "I've created dashboards to track KPIs"
✅ "I know how to instrument code with metrics"
✅ "I understand alerting concepts"

❌ They DON'T expect you to be Prometheus expert
❌ They DON'T expect you to know all monitoring tools
❌ They DON'T expect production-scale experience

**2 days of hands-on with Prometheus + Grafana = enough to pass interviews!**

---

## 🚀 Start RIGHT NOW

**Next 30 Minutes:**
```bash
# 1. Create folder
mkdir monitoring-demo
cd monitoring-demo

# 2. Create docker-compose.yml (copy from above)

# 3. Create prometheus.yml (copy from above)

# 4. Start
docker-compose up -d

# 5. Access
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)

# Done! You're monitoring!
```

**This Weekend:**
- Saturday: Complete Day 1 (Prometheus)
- Sunday: Complete Day 2 (Grafana)
- Monday: Update resume, add to LinkedIn

**You'll be able to honestly say:** 
"I have hands-on experience with Prometheus and Grafana for application and infrastructure monitoring."

**That's ALL you need! 🎉**
