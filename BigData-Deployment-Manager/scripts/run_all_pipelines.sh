#!/bin/bash

# ============================================================
# Run All Deployment Manager Pipelines
# Executes NetOps and 5G Core analytics then starts API
# ============================================================

set -e  # Exit on error

echo "============================================================"
echo "DEPLOYMENT MANAGER - Complete Pipeline Execution"
echo "============================================================"
echo "Start Time: $(date)"
echo "============================================================"

# Set project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Step 1: Run NetOps Analytics
echo ""
echo "============================================================"
echo "STEP 1: Running NetOps Deployment Analytics"
echo "============================================================"
python pyspark_jobs/netops/deployment_analytics.py

if [ $? -eq 0 ]; then
    echo "✓ NetOps analytics completed successfully"
else
    echo "✗ NetOps analytics failed"
    exit 1
fi

# Step 2: Run 5G Core Analytics
echo ""
echo "============================================================"
echo "STEP 2: Running 5G Core Registration Analytics"
echo "============================================================"
python pyspark_jobs/core5g/registration_analytics.py

if [ $? -eq 0 ]; then
    echo "✓ 5G Core analytics completed successfully"
else
    echo "✗ 5G Core analytics failed"
    exit 1
fi

# Step 3: Start Flask API
echo ""
echo "============================================================"
echo "STEP 3: Starting Flask API Server"
echo "============================================================"
echo "API will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "============================================================"

python api/app.py &
API_PID=$!

echo "Flask API started with PID: $API_PID"

# Wait for API to start
sleep 5

# Test API health
echo ""
echo "Testing API health endpoint..."
curl -s http://localhost:5000/api/health | python -m json.tool

echo ""
echo "============================================================"
echo "✓ ALL PIPELINES COMPLETED SUCCESSFULLY"
echo "============================================================"
echo "API Endpoints Available:"
echo "  - Health:          http://localhost:5000/api/health"
echo "  - Overview:        http://localhost:5000/api/deployment-manager/overview"
echo "  - NetOps:          http://localhost:5000/api/netops/deployments"
echo "  - 5G Core:         http://localhost:5000/api/5g/registration-kpis"
echo "  - Statistics:      http://localhost:5000/api/stats/summary"
echo "============================================================"
echo "End Time: $(date)"
echo "============================================================"

# Keep the script running
wait $API_PID
