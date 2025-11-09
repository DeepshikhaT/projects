# Big Data Deployment Manager - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you quickly set up and run the Big Data Deployment Manager for analyzing NetOps and 5G Core deployments.

---

## Prerequisites

Before starting, ensure you have:

- ✅ Python 3.8 or higher
- ✅ Java 11+ (for Spark)
- ✅ PostgreSQL 13+ (or use Docker)
- ✅ 8GB+ RAM available

---

## Option 1: Quick Setup with Docker (Recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/DeepshikhaT/Python_Data_Engineer.git
cd BigData-Deployment-Manager
```

### Step 2: Start Services with Docker

```bash
cd docker
docker-compose up -d
```

This will start:
- PostgreSQL database
- Spark Master & Worker
- Hive Metastore
- Flask API
- Redis (optional)

### Step 3: Verify Services

```bash
# Check if all services are running
docker-compose ps

# Test API health
curl http://localhost:5000/api/health
```

### Step 4: Access Services

- **Flask API**: http://localhost:5000
- **Spark UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432

---

## Option 2: Local Setup (Without Docker)

### Step 1: Install Dependencies

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

### Step 2: Configure Database

Edit `config/database_config.yaml`:

```yaml
source_db:
  host: "localhost"
  port: 5432
  database: "netops_db"
  user: "your_username"
  password: "your_password"
```

### Step 3: Set Up PostgreSQL

```bash
# Create database
createdb netops_db
createdb core5g_db

# Create tables (if you have the SQL script)
psql -U postgres -d netops_db -f sql/create_tables.sql
```

### Step 4: Configure Spark

Edit `config/spark_config.yaml`:

```yaml
spark:
  master: "local[4]"  # Use local mode with 4 cores
  executor_memory: "4g"
  executor_cores: 4
```

---

## Running the Pipeline

### Option A: Run Complete Pipeline

```bash
# Make script executable (Linux/Mac)
chmod +x scripts/run_all_pipelines.sh

# Run all pipelines
bash scripts/run_all_pipelines.sh
```

### Option B: Run Individual Components

**1. NetOps Analytics**
```bash
python pyspark_jobs/netops/deployment_analytics.py
```

**2. 5G Core Analytics**
```bash
python pyspark_jobs/core5g/registration_analytics.py
```

**3. Start Flask API**
```bash
python api/app.py
```

---

## Testing the API

### Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "service": "Deployment Manager API",
  "version": "1.0.0"
}
```

### Get Deployment Overview

```bash
curl http://localhost:5000/api/deployment-manager/overview?days=7
```

### Get NetOps Deployments

```bash
curl "http://localhost:5000/api/netops/deployments?start_date=2024-01-01&end_date=2024-01-15"
```

### Get 5G Registration KPIs

```bash
curl "http://localhost:5000/api/5g/registration-kpis?days=7"
```

### Get Statistics Summary

```bash
curl http://localhost:5000/api/stats/summary?days=7
```

---

## Integration with Existing Projects

### Integrate with NetOps-Automation

1. **Ensure your NetOps-Automation is logging to PostgreSQL**

   Check `NetOps-Automation/api/ansible_api_with_db.py` is writing to the database.

2. **Configure database connection**

   Update `config/database_config.yaml` to point to your NetOps database.

3. **Run NetOps analytics**

   ```bash
   python pyspark_jobs/netops/deployment_analytics.py
   ```

### Integrate with 5G-Core-Automation

1. **Ensure 5G Core telemetry is being collected**

   Your AMF, SMF, and other NFs should be logging telemetry data.

2. **Configure 5G database connection**

   Update `core5g_db` section in `config/database_config.yaml`.

3. **Run 5G analytics**

   ```bash
   python pyspark_jobs/core5g/registration_analytics.py
   ```

---

## Sample Data (For Testing)

If you don't have real data yet, you can generate sample data:

### Create Sample NetOps Data

```sql
-- Connect to netops_db
CREATE TABLE IF NOT EXISTS ansible_execution_logs (
    id SERIAL PRIMARY KEY,
    playbook VARCHAR(255),
    site_id VARCHAR(100),
    status VARCHAR(50),
    duration_seconds FLOAT,
    error_message TEXT,
    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO ansible_execution_logs (playbook, site_id, status, duration_seconds)
VALUES
    ('configure_vlans.yml', 'SITE001', 'success', 45.2),
    ('configure_ospf.yml', 'SITE001', 'success', 32.1),
    ('backup_configs.yml', 'SITE002', 'failed', 12.5),
    ('health_check.yml', 'SITE003', 'success', 8.9);
```

### Create Sample 5G Core Data

```sql
-- Connect to core5g_db
CREATE TABLE IF NOT EXISTS amf_registration_events (
    id SERIAL PRIMARY KEY,
    site_id VARCHAR(100),
    amf_instance VARCHAR(100),
    result VARCHAR(50),
    latency_ms FLOAT,
    failure_reason TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO amf_registration_events (site_id, amf_instance, result, latency_ms)
VALUES
    ('SITE001', 'amf-01', 'SUCCESS', 45.2),
    ('SITE001', 'amf-01', 'SUCCESS', 38.5),
    ('SITE002', 'amf-02', 'FAILED', 120.0),
    ('SITE003', 'amf-03', 'SUCCESS', 42.1);
```

---

## API Endpoints Reference

### General Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/deployment-manager/overview` | GET | Overall deployment health |
| `/api/deployment-manager/sites/{site_id}` | GET | Site-specific details |
| `/api/stats/summary` | GET | Summary statistics |

### NetOps Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/netops/deployments` | GET | Deployment statistics |
| `/api/netops/deployment-trends` | GET | Trends over time |
| `/api/netops/failures` | GET | Deployment failures |

### 5G Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/5g/registration-kpis` | GET | Registration KPIs |
| `/api/5g/registration-failures` | GET | Registration failures |

---

## Troubleshooting

### Issue: Spark Out of Memory

**Solution:**
```yaml
# In config/spark_config.yaml, increase memory
executor_memory: "8g"
driver_memory: "4g"
```

### Issue: Database Connection Failed

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify credentials in config/database_config.yaml
# Test connection
psql -U postgres -h localhost -d netops_db
```

### Issue: API Returns Empty Results

**Solution:**
```bash
# Ensure you've run the PySpark jobs first
python pyspark_jobs/netops/deployment_analytics.py

# Check if Hive tables exist
# Start Spark SQL shell
spark-sql
> SHOW DATABASES;
> USE deployment_analytics;
> SHOW TABLES;
> SELECT COUNT(*) FROM ansible_deployment_metrics;
```

### Issue: Hive Metastore Not Found

**Solution:**
```bash
# Using Docker: restart hive-metastore
docker-compose restart hive-metastore

# Local setup: ensure Hive is configured
# Check config/database_config.yaml for metastore_uri
```

---

## Next Steps

1. **Customize Analytics**: Modify PySpark jobs in `pyspark_jobs/` to add custom metrics

2. **Add More Endpoints**: Extend Flask API in `api/app.py` with new endpoints

3. **Create Dashboard**: Build a React/Vue dashboard to visualize the data

4. **Schedule Jobs**: Use cron or Airflow to run analytics periodically

5. **Deploy to Cloud**: Deploy to AWS EMR, GCP Dataproc, or Azure HDInsight

---

## Example Use Cases

### Use Case 1: Monitor Deployment Success Rate

```bash
# Get last 30 days deployment trends
curl "http://localhost:5000/api/netops/deployment-trends?days=30"

# Identify failing sites
curl "http://localhost:5000/api/netops/failures?limit=10"
```

### Use Case 2: Track 5G Core Performance

```bash
# Get registration KPIs for specific site
curl "http://localhost:5000/api/5g/registration-kpis?site_id=SITE001&days=7"

# Analyze failure patterns
curl "http://localhost:5000/api/5g/registration-failures?limit=20"
```

### Use Case 3: Generate Daily Reports

```bash
# Create a script to fetch daily stats
#!/bin/bash
DATE=$(date +%Y-%m-%d)
curl "http://localhost:5000/api/stats/summary?days=1" > report_${DATE}.json
```

---

## Performance Tips

1. **Partition Your Data**: Hive tables are partitioned by date for efficient queries

2. **Use Caching**: Add Redis caching for frequently accessed data

3. **Optimize Spark**: Tune executor memory and cores based on workload

4. **Index Database**: Add indexes on frequently queried columns in PostgreSQL

5. **Aggregate First**: Pre-compute aggregations in PySpark jobs

---

## Support & Documentation

- **Full Documentation**: See `README.md`
- **API Reference**: See `docs/API_REFERENCE.md`
- **Architecture**: See `docs/ARCHITECTURE.md`
- **GitHub Issues**: https://github.com/DeepshikhaT/Python_Data_Engineer/issues

---

## Summary

You've successfully set up the Big Data Deployment Manager! 🎉

This project demonstrates:
- ✅ Big data processing with PySpark
- ✅ Data warehousing with Hive
- ✅ RESTful API development with Flask
- ✅ Integration with existing deployment systems
- ✅ End-to-end data engineering pipeline

**Next**: Start analyzing your deployment data and building dashboards!
