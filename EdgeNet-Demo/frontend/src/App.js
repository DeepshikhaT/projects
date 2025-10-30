import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Dashboard from './components/Dashboard';
import DeploymentList from './components/DeploymentList';
import AuditLog from './components/AuditLog';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState(null);
  const [deployments, setDeployments] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, deploymentsRes, auditRes] = await Promise.all([
        axios.get('/api/stats'),
        axios.get('/api/deployments'),
        axios.get('/api/audit?limit=20')
      ]);

      setStats(statsRes.data);
      setDeployments(deploymentsRes.data);
      setAuditLogs(auditRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🌐 EdgeNet-Demo</h1>
        <p>Automated Network Deployment & Monitoring</p>
      </header>

      <nav className="app-nav">
        <button
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={activeTab === 'deployments' ? 'active' : ''}
          onClick={() => setActiveTab('deployments')}
        >
          Deployments
        </button>
        <button
          className={activeTab === 'audit' ? 'active' : ''}
          onClick={() => setActiveTab('audit')}
        >
          Audit Logs
        </button>
      </nav>

      <main className="app-content">
        {activeTab === 'dashboard' && <Dashboard stats={stats} />}
        {activeTab === 'deployments' && (
          <DeploymentList deployments={deployments} onRefresh={fetchData} />
        )}
        {activeTab === 'audit' && <AuditLog logs={auditLogs} />}
      </main>

      <footer className="app-footer">
        <p>Created by Deepshikha Tripathi | EdgeNet-Demo v1.0</p>
      </footer>
    </div>
  );
}

export default App;
