# Big Data Deployment Manager

## Overview

A comprehensive big data analytics platform for deployment management that processes and analyzes deployment data from NetOps and 5G Core infrastructure. This project demonstrates end-to-end data engineering capabilities including data ingestion, processing with PySpark, storage in Hive, and serving data through REST APIs.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT MANAGER SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [DEPLOYMENT LAYER]                                             │
│  ├── Ansible Playbooks (NetOps-Automation)                     │
│  ├── Kubernetes/Helm (5G-Core-Automation)                      │
│  └── Configuration Management                                   │
│                          ↓                                      │
│  [DATA COLLECTION LAYER]                                        │
│  ├── Ansible Execution Logs                                    │
│  ├── Device Metrics (SNMP, Syslog)                             │
│  ├── 5G Core Telemetry (CDRs, Signaling)                       │
│  ├── Container Metrics (Prometheus)                            │
│  └── Configuration Backups                                      │
│                          ↓                                      │
│  [RAW DATA STORAGE]                                             │
│  └── PostgreSQL (Time-series and event data)                   │
│                          ↓                                      │
│  [BIG DATA PROCESSING - PySpark]                                │
│  ├── Deployment Success Analytics                              │
│  ├── Device Health Scoring                                     │
│  ├── 5G Core KPI Calculation                                   │
│  ├── Configuration Drift Detection                             │
│  └── Anomaly Detection                                          │
│                          ↓                                      │
│  [DATA WAREHOUSE - Hive]                                        │
│  └── Partitioned by date, site, device_type                    │
│                          ↓                                      │
│  [API LAYER - Flask]                                            │
│  └── REST APIs for Deployment Dashboard                        │
│                          ↓                                      │
│  [DASHBOARD]                                                    │
│  ├── Deployment Status Overview                                │
│  ├── Site Health Monitoring                                    │
│  ├── KPI Dashboards                                            │
│  └── Alert Management                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Features

### ✅ NetOps Deployment Analytics
- Track Ansible playbook execution success rates
- Monitor device health across all sites
- Detect configuration drift automatically
- Analyze deployment trends and patterns
- Identify problematic deployments

### ✅ 5G Core Deployment Analytics
- Calculate registration success rates
- Track call setup and handover KPIs
- Monitor Network Function (NF) performance
- Analyze call detail records (CDRs)
- Measure QoS metrics

### ✅ Big Data Processing
- PySpark for scalable data processing
- Hive for data warehousing
- Partitioned storage for efficient queries
- Batch and streaming capabilities

### ✅ REST API
- RESTful endpoints for all metrics
- Real-time deployment status
- Historical trend analysis
- Site-specific analytics
- Failure tracking and reporting

## Project Structure

```
BigData-Deployment-Manager/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
│
├── config/
│   ├── spark_config.yaml          # Spark configuration
│   ├── database_config.yaml       # Database connections
│   └── hive_config.yaml           # Hive warehouse settings
│
├── pyspark_jobs/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── spark_session.py      # Spark session factory
│   │   └── utils.py               # Common utilities
│   │
│   ├── netops/
│   │   ├── __init__.py
│   │   ├── deployment_analytics.py    # Ansible deployment analysis
│   │   ├── device_health.py           # Device health scoring
│   │   └── config_drift.py            # Configuration drift detection
│   │
│   └── core5g/
│       ├── __init__.py
│       ├── registration_analytics.py  # Registration KPI analysis
│       ├── call_analytics.py          # Call success analysis
│       └── nf_performance.py          # NF performance analysis
│
├── api/
│   ├── __init__.py
│   ├── app.py                     # Flask application
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── deployment_routes.py   # Deployment endpoints
│   │   ├── netops_routes.py       # NetOps specific endpoints
│   │   └── core5g_routes.py       # 5G Core endpoints
│   ├── models.py                  # Data models
│   └── utils.py                   # API utilities
│
├── scripts/
│   ├── setup_environment.sh       # Environment setup
│   ├── setup_hive_tables.sh       # Hive table creation
│   ├── run_netops_pipeline.sh     # Run NetOps ETL
│   ├── run_5g_pipeline.sh         # Run 5G ETL
│   └── run_all_pipelines.sh       # Run complete pipeline
│
├── sql/
│   ├── create_tables.sql          # Table definitions
│   ├── netops_views.sql           # NetOps views
│   └── core5g_views.sql           # 5G Core views
│
├── tests/
│   ├── test_spark_jobs.py
│   ├── test_api.py
│   └── test_integration.py
│
├── docker/
│   ├── Dockerfile.spark           # Spark container
│   ├── Dockerfile.api             # API container
│   ├── docker-compose.yml         # Complete stack
│   └── postgres-init.sql          # Database initialization
│
└── docs/
    ├── DEPLOYMENT.md              # Deployment guide
    ├── API_REFERENCE.md           # API documentation
    └── ARCHITECTURE.md            # Architecture details
```

## Prerequisites

- Python 3.8+
- Apache Spark 3.5+
- Apache Hive 3.x (or compatible data warehouse)
- PostgreSQL 13+ (or other RDBMS)
- Java 11+ (for Spark)
- 8GB+ RAM recommended

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DeepshikhaT/Python_Data_Engineer.git
cd BigData-Deployment-Manager
```

### 2. Set up Python environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Configure database connections, Spark settings, etc.
```

### 4. Set up databases

```bash
# Initialize PostgreSQL database
psql -U postgres -f docker/postgres-init.sql

# Set up Hive tables
bash scripts/setup_hive_tables.sh
```

### 5. Configure Spark

Edit `config/spark_config.yaml` with your Spark cluster settings:

```yaml
spark:
  master: "local[4]"  # or your cluster URL
  app_name: "DeploymentManagerETL"
  executor_memory: "4g"
  executor_cores: 4
```

## Usage

### Run Complete Pipeline

```bash
# Run all ETL jobs and start API
bash scripts/run_all_pipelines.sh
```

### Run Individual Components

**NetOps Analytics:**
```bash
bash scripts/run_netops_pipeline.sh
```

**5G Core Analytics:**
```bash
bash scripts/run_5g_pipeline.sh
```

**API Server:**
```bash
python api/app.py
```

### Using Docker

```bash
# Start complete stack
cd docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop stack
docker-compose down
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Deployment Overview
```
GET /api/deployment-manager/overview
Response: Overall deployment health across all sites
```

### Site Details
```
GET /api/deployment-manager/sites/{site_id}
Response: Detailed metrics for specific site
```

### NetOps Endpoints

**Deployment Metrics**
```
GET /api/netops/deployments?start_date=2024-01-01&end_date=2024-12-31
Response: Ansible deployment statistics
```

**Device Health**
```
GET /api/netops/device-health?site_id=SITE001
Response: Device health scores and metrics
```

**Configuration Drift**
```
GET /api/netops/config-drift
Response: Devices with configuration drift
```

### 5G Core Endpoints

**Registration KPIs**
```
GET /api/5g/registration-kpis?site_id=SITE001
Response: UE registration success rates and latency
```

**Call Metrics**
```
GET /api/5g/call-metrics?start_date=2024-01-01
Response: Call success rates and statistics
```

**NF Performance**
```
GET /api/5g/nf-performance?nf_type=AMF
Response: Network Function performance metrics
```

## Integration with Existing Projects

### NetOps-Automation Integration

This project reads data from your NetOps-Automation:
- Ansible execution logs from `ansible_api_with_db.py`
- Device metrics from `network_monitor.py`
- Configuration backups from playbooks

**Data Flow:**
```
NetOps-Automation → PostgreSQL → PySpark → Hive → API
```

### 5G-Core-Automation Integration

Processes telemetry from 5G Core:
- Registration events from AMF
- Call detail records from SMF
- Performance metrics from all NFs

**Data Flow:**
```
5G-Core-Automation → Telemetry DB → PySpark → Hive → API
```

## Configuration

### Database Configuration (`config/database_config.yaml`)

```yaml
source_db:
  host: "localhost"
  port: 5432
  database: "deployment_db"
  user: "postgres"
  password: "your_password"

hive:
  metastore_uri: "thrift://localhost:9083"
  warehouse_dir: "/user/hive/warehouse"
  database: "deployment_analytics"
```

### Spark Configuration (`config/spark_config.yaml`)

```yaml
spark:
  master: "local[4]"
  app_name: "DeploymentManagerETL"
  executor_memory: "4g"
  executor_cores: 4
  dynamic_allocation: true
  sql:
    warehouse_dir: "/user/hive/warehouse"
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_spark_jobs.py
pytest tests/test_api.py

# Run with coverage
pytest --cov=pyspark_jobs --cov=api tests/
```

## Performance Optimization

### Spark Optimizations
- Partitioning by date for efficient queries
- Broadcast joins for small dimension tables
- Dynamic partition pruning
- Adaptive query execution

### Hive Optimizations
- ORC file format for compression
- Partitioned tables by date and site
- Statistics collection for CBO
- Vectorized query execution

## Monitoring

### Spark UI
Access at: `http://localhost:4040` (when Spark job is running)

### API Metrics
```
GET /api/metrics
Response: API performance metrics
```

## Troubleshooting

### Common Issues

**1. Spark out of memory**
- Increase executor memory in `spark_config.yaml`
- Reduce partition size
- Enable dynamic allocation

**2. Hive connection issues**
- Check metastore service is running
- Verify `hive_config.yaml` settings
- Check network connectivity

**3. API slow response**
- Add caching layer (Redis)
- Optimize Hive queries
- Create materialized views

## Deployment

### Production Deployment

**AWS:**
- EMR for Spark jobs
- RDS for PostgreSQL
- Athena or EMR Hive
- ECS/Fargate for API

**GCP:**
- Dataproc for Spark
- Cloud SQL for PostgreSQL
- BigQuery instead of Hive
- Cloud Run for API

**Azure:**
- HDInsight for Spark
- Azure Database for PostgreSQL
- Synapse Analytics
- App Service for API

## Skills Demonstrated

### Data Engineering
- ✅ Big data processing with PySpark
- ✅ Data warehousing (Hive)
- ✅ ETL pipeline design
- ✅ Data modeling and partitioning
- ✅ Performance optimization

### Automation
- ✅ Pipeline orchestration
- ✅ Configuration management
- ✅ Shell scripting
- ✅ CI/CD integration

### API Development
- ✅ REST API design
- ✅ Flask framework
- ✅ Error handling
- ✅ API documentation

### Integration
- ✅ Integration with existing systems
- ✅ Multi-source data ingestion
- ✅ Microservices architecture

## Contributing

This is a portfolio project demonstrating data engineering capabilities for deployment management in network operations and 5G infrastructure.

## License

MIT License

## Author

Deepshikha T - Data Engineer specializing in big data processing and automation

## Contact

GitHub: [@DeepshikhaT](https://github.com/DeepshikhaT)

---

**Note:** This project demonstrates end-to-end data engineering skills applicable to telecom, network operations, and large-scale infrastructure management.
