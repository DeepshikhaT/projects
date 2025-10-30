import React, { useState } from 'react';
import axios from 'axios';
import './DeploymentList.css';

function DeploymentList({ deployments, onRefresh }) {
  const [expandedDeployment, setExpandedDeployment] = useState(null);
  const [newDeploymentName, setNewDeploymentName] = useState('');

  const handleCreateDeployment = async (e) => {
    e.preventDefault();
    if (!newDeploymentName.trim()) return;

    try {
      await axios.post('/api/deployments', {
        name: newDeploymentName,
        status: 'active'
      });
      setNewDeploymentName('');
      onRefresh();
    } catch (error) {
      alert('Error creating deployment: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDeleteDeployment = async (id) => {
    if (!window.confirm('Are you sure you want to delete this deployment?')) return;

    try {
      await axios.delete(`/api/deployments/${id}`);
      onRefresh();
    } catch (error) {
      alert('Error deleting deployment: ' + error.message);
    }
  };

  const getStatusBadge = (status) => {
    const statusColors = {
      'active': '#43e97b',
      'pending': '#feca57',
      'inactive': '#fa709a',
      'online': '#43e97b',
      'offline': '#fa709a',
      'maintenance': '#feca57'
    };

    return (
      <span
        className="status-badge"
        style={{ backgroundColor: statusColors[status] || '#999' }}
      >
        {status}
      </span>
    );
  };

  return (
    <div className="deployment-list">
      <div className="deployment-header">
        <h2>Deployments</h2>
        <form onSubmit={handleCreateDeployment} className="create-form">
          <input
            type="text"
            placeholder="New deployment name..."
            value={newDeploymentName}
            onChange={(e) => setNewDeploymentName(e.target.value)}
          />
          <button type="submit">+ Create Deployment</button>
        </form>
      </div>

      {deployments.length === 0 ? (
        <div className="empty-state">
          <p>No deployments found. Create one to get started!</p>
        </div>
      ) : (
        <div className="deployments">
          {deployments.map((deployment) => (
            <div key={deployment.id} className="deployment-card">
              <div className="deployment-info">
                <div className="deployment-main">
                  <h3>{deployment.name}</h3>
                  {getStatusBadge(deployment.status)}
                </div>
                <div className="deployment-meta">
                  <span>ID: {deployment.id}</span>
                  <span>Subdeployments: {deployment.subdeployments?.length || 0}</span>
                </div>
              </div>

              <div className="deployment-actions">
                <button
                  onClick={() => setExpandedDeployment(
                    expandedDeployment === deployment.id ? null : deployment.id
                  )}
                  className="btn-expand"
                >
                  {expandedDeployment === deployment.id ? '▲ Hide' : '▼ Show'} Details
                </button>
                <button
                  onClick={() => handleDeleteDeployment(deployment.id)}
                  className="btn-delete"
                >
                  🗑️ Delete
                </button>
              </div>

              {expandedDeployment === deployment.id && (
                <div className="deployment-details">
                  <h4>Subdeployments ({deployment.subdeployments?.length || 0})</h4>
                  {deployment.subdeployments && deployment.subdeployments.length > 0 ? (
                    deployment.subdeployments.map((subdep) => (
                      <div key={subdep.id} className="subdep-card">
                        <div className="subdep-header">
                          <h5>{subdep.name}</h5>
                          {getStatusBadge(subdep.status)}
                        </div>
                        <p>Hosts: {subdep.mhosts?.length || 0}</p>
                        {subdep.mhosts && subdep.mhosts.length > 0 && (
                          <div className="mhosts-list">
                            {subdep.mhosts.map((mhost) => (
                              <div key={mhost.id} className="mhost-item">
                                <span className="mhost-name">{mhost.hostname}</span>
                                {getStatusBadge(mhost.status)}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <p className="empty-subdeps">No subdeployments yet</p>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DeploymentList;
