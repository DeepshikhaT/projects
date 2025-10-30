# EdgeNet-Demo Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Start the Backend

```bash
# Navigate to backend directory
cd EdgeNet-Demo/backend

# Install Python dependencies
pip install flask flask-sqlalchemy flask-cors requests

# Run the server
python app.py
```

Backend will be running at `http://localhost:5000`

### Step 2: Start the Frontend

Open a new terminal:

```bash
# Navigate to frontend directory
cd EdgeNet-Demo/frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Frontend will automatically open at `http://localhost:3000`

### Step 3: Add Sample Data

Open a third terminal:

```bash
# Navigate to backend directory
cd EdgeNet-Demo/backend

# Create sample deployments
python automation.py setup
```

This creates:
- 3 Deployments (Production, Staging, Development)
- Multiple subdeployments per deployment
- Multiple hosts per subdeployment

### Step 4: Explore the Application

1. **Dashboard Tab**: View system statistics and network health
2. **Deployments Tab**:
   - See all deployments with hierarchical structure
   - Click "Show Details" to expand and view subdeployments and hosts
   - Create new deployments using the form
   - Delete deployments (cascades to subdeployments and hosts)
3. **Audit Logs Tab**: View all system actions with timestamps

### Optional: Start Monitoring Simulation

```bash
cd EdgeNet-Demo/backend
python automation.py monitor
```

This will continuously update host statuses every 5 seconds, simulating a real monitoring system.

## 🎯 What to Test

### Via Web UI
1. Create a new deployment
2. View the updated statistics on the dashboard
3. Check audit logs for the creation event
4. Expand a deployment to see its structure
5. Delete a deployment and see it removed

### Via API
```bash
# Create a deployment
curl -X POST http://localhost:5000/api/deployments \
  -H "Content-Type: application/json" \
  -d '{"name": "TestDeployment", "status": "active"}'

# Get all deployments
curl http://localhost:5000/api/deployments

# Get statistics
curl http://localhost:5000/api/stats
```

## 📦 What's Included

- ✅ Complete Flask REST API with CRUD operations
- ✅ SQLAlchemy models with relationships
- ✅ React frontend with real-time updates
- ✅ Automated testing suite
- ✅ Automation scripts for bulk operations
- ✅ Audit logging system
- ✅ Beautiful, responsive UI

## 💡 Tips

- The frontend auto-refreshes data every 5 seconds
- All database operations are automatically logged in audit logs
- The database is SQLite-based (edgenet.db) and created automatically
- Run tests with: `cd backend && python -m unittest tests/test_api.py`

Enjoy exploring EdgeNet-Demo! 🌐
