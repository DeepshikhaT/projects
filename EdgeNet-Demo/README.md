# EdgeNet-Demo: Automated Network Deployment & Monitoring

## Overview
EdgeNet-Demo is a full-stack application that simulates automated network deployment, configuration, and monitoring. It demonstrates professional software development skills including RESTful API design, database modeling, automated testing, real-time monitoring, and modern React frontend development.

## Key Features
- 🚀 **Deployment Management**: Create and manage hierarchical deployments, subdeployments, and network hosts
- 🔄 **Automated Configuration**: Python automation scripts for bulk operations and monitoring
- 📊 **Real-time Dashboard**: Live statistics and network health monitoring
- 📝 **Audit Logging**: Complete audit trail for all system actions
- ✅ **Comprehensive Testing**: Full test suite with unittest
- 🎨 **Modern UI**: Responsive React frontend with beautiful gradient design

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Testing**: unittest
- **CORS**: flask-cors for cross-origin requests

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Build Tool**: React Scripts
- **Styling**: CSS3 with modern gradients and animations

## Project Structure
```
EdgeNet-Demo/
├── backend/
│   ├── app.py              # Flask application factory
│   ├── models.py           # Database models
│   ├── routes.py           # API endpoints
│   ├── config.py           # Configuration settings
│   ├── automation.py       # Automation and monitoring scripts
│   └── tests/
│       └── test_api.py     # API test suite
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js        # Dashboard component
│   │   │   ├── DeploymentList.js   # Deployments view
│   │   │   └── AuditLog.js         # Audit logs view
│   │   ├── App.js          # Main application component
│   │   └── index.js        # Application entry point
│   └── package.json
├── README.md
├── design.md
└── requirement.txt
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r ../requirement.txt
   ```

5. **Run the backend server**:
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:3000` and automatically open in your browser

## Usage

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Navigate between tabs:
   - **Dashboard**: View system statistics and network health
   - **Deployments**: Create and manage deployments
   - **Audit Logs**: View system activity logs

### API Endpoints

#### Deployments
- `GET /api/deployments` - List all deployments
- `POST /api/deployments` - Create a new deployment
- `GET /api/deployments/<id>` - Get deployment details
- `PUT /api/deployments/<id>` - Update deployment
- `DELETE /api/deployments/<id>` - Delete deployment

#### Subdeployments
- `GET /api/subdeployments` - List all subdeployments
- `POST /api/subdeployments` - Create a new subdeployment
- `PUT /api/subdeployments/<id>` - Update subdeployment
- `DELETE /api/subdeployments/<id>` - Delete subdeployment

#### Mhosts
- `GET /api/mhosts` - List all hosts
- `POST /api/mhosts` - Create a new host
- `PUT /api/mhosts/<id>` - Update host
- `DELETE /api/mhosts/<id>` - Delete host

#### Audit & Stats
- `GET /api/audit` - Get audit logs
- `GET /api/stats` - Get system statistics

### Automation Scripts

The `automation.py` script provides powerful automation capabilities:

1. **Setup Sample Data**:
   ```bash
   cd backend
   python automation.py setup
   ```
   Creates sample deployments with subdeployments and hosts

2. **Start Monitoring Simulation**:
   ```bash
   python automation.py monitor
   ```
   Simulates real-time host status changes every 5 seconds

3. **View Statistics**:
   ```bash
   python automation.py stats
   ```
   Display current system statistics

4. **View Audit Logs**:
   ```bash
   python automation.py audit
   ```
   Display recent audit log entries

## Running Tests

### Backend Tests

```bash
cd backend
python -m unittest tests/test_api.py
```

The test suite includes:
- Deployment CRUD operations
- Subdeployment management
- Host management
- Audit logging
- Statistics calculation
- Error handling

## Skills Demonstrated

### Backend Development
- ✅ RESTful API design with Flask
- ✅ Database modeling with SQLAlchemy
- ✅ ORM relationships (one-to-many, cascade deletes)
- ✅ Error handling and validation
- ✅ Automated testing with unittest
- ✅ Audit logging and tracking

### Frontend Development
- ✅ Modern React with hooks (useState, useEffect)
- ✅ Component architecture
- ✅ API integration with Axios
- ✅ Real-time data updates
- ✅ Responsive design
- ✅ User interaction handling

### Software Engineering
- ✅ Project structure and organization
- ✅ Separation of concerns
- ✅ Configuration management
- ✅ Documentation
- ✅ Testing methodology
- ✅ Automation scripting

## API Examples

### Create a Deployment
```bash
curl -X POST http://localhost:5000/api/deployments \
  -H "Content-Type: application/json" \
  -d '{"name": "Production", "status": "active"}'
```

### Create a Subdeployment
```bash
curl -X POST http://localhost:5000/api/subdeployments \
  -H "Content-Type: application/json" \
  -d '{"name": "Web-Servers", "deployment_id": 1, "status": "active"}'
```

### Create a Host
```bash
curl -X POST http://localhost:5000/api/mhosts \
  -H "Content-Type: application/json" \
  -d '{"hostname": "web-01.example.com", "subdeployment_id": 1, "status": "online"}'
```

## Future Enhancements
- Authentication and authorization
- WebSocket integration for real-time updates
- Advanced filtering and search
- Export functionality (CSV, JSON)
- Docker containerization
- CI/CD pipeline integration
- Performance monitoring
- More comprehensive test coverage

## Author
**Deepshikha Tripathi**

This project demonstrates proficiency in:
- Full-stack development
- Python/Flask backend development
- React frontend development
- RESTful API design
- Database design and ORM usage
- Testing and automation
- Modern web development practices

## License
This is a demonstration project for portfolio purposes.
