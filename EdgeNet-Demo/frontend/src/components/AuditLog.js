import React from 'react';
import './AuditLog.css';

function AuditLog({ logs }) {
  if (!logs || logs.length === 0) {
    return (
      <div className="audit-log">
        <h2>Audit Logs</h2>
        <div className="empty-state">
          <p>No audit logs available yet.</p>
        </div>
      </div>
    );
  }

  const getActionColor = (action) => {
    const colors = {
      'created': '#43e97b',
      'updated': '#4facfe',
      'deleted': '#fa709a'
    };
    return colors[action] || '#999';
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="audit-log">
      <h2>Audit Logs</h2>
      <div className="logs-container">
        {logs.map((log) => (
          <div key={log.id} className="log-entry">
            <div className="log-header">
              <span
                className="action-badge"
                style={{ backgroundColor: getActionColor(log.action) }}
              >
                {log.action}
              </span>
              <span className="entity-type">{log.entity_type}</span>
              <span className="entity-id">#{log.entity_id}</span>
            </div>
            {log.details && (
              <div className="log-details">{log.details}</div>
            )}
            <div className="log-timestamp">{formatTimestamp(log.timestamp)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AuditLog;
