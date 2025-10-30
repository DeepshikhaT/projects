import React from 'react';
import './Dashboard.css';

function Dashboard({ stats }) {
  if (!stats) {
    return <div className="loading">Loading statistics...</div>;
  }

  const statCards = [
    {
      title: 'Total Deployments',
      value: stats.total_deployments,
      icon: '🚀',
      color: '#667eea'
    },
    {
      title: 'Total Subdeployments',
      value: stats.total_subdeployments,
      icon: '📦',
      color: '#f093fb'
    },
    {
      title: 'Total Hosts',
      value: stats.total_mhosts,
      icon: '🖥️',
      color: '#4facfe'
    },
    {
      title: 'Active Hosts',
      value: stats.active_mhosts,
      icon: '✅',
      color: '#43e97b'
    },
    {
      title: 'Offline Hosts',
      value: stats.offline_mhosts,
      icon: '❌',
      color: '#fa709a'
    }
  ];

  return (
    <div className="dashboard">
      <h2>System Overview</h2>
      <div className="stats-grid">
        {statCards.map((stat, index) => (
          <div key={index} className="stat-card" style={{ borderColor: stat.color }}>
            <div className="stat-icon" style={{ color: stat.color }}>
              {stat.icon}
            </div>
            <div className="stat-info">
              <h3>{stat.title}</h3>
              <p className="stat-value">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-info">
        <h3>📊 Network Health</h3>
        <div className="health-bar">
          <div
            className="health-fill"
            style={{
              width: `${stats.total_mhosts > 0 ? (stats.active_mhosts / stats.total_mhosts) * 100 : 0}%`,
              background: stats.active_mhosts / stats.total_mhosts > 0.7 ? '#43e97b' :
                         stats.active_mhosts / stats.total_mhosts > 0.4 ? '#feca57' : '#fa709a'
            }}
          />
        </div>
        <p className="health-text">
          {stats.total_mhosts > 0
            ? `${Math.round((stats.active_mhosts / stats.total_mhosts) * 100)}% of hosts are online`
            : 'No hosts configured'}
        </p>
      </div>
    </div>
  );
}

export default Dashboard;
