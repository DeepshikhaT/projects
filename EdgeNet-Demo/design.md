# Project Design: EdgeNet-Demo

## Data Model

- **Deployment**
  - id (int, PK)
  - name (string)
  - status (string)

- **Subdeployment**
  - id (int, PK)
  - deployment_id (int, FK)
  - name (string)
  - status (string)

- **Mhost**
  - id (int, PK)
  - subdeployment_id (int, FK)
  - hostname (string)
  - config (string)
  - status (string)

- **AuditLog**
  - id (int, PK)
  - entity_type (string)
  - entity_id (int)
  - action (string)
  - timestamp (datetime)

## API Endpoints

- `/deployments` (GET, POST)
- `/subdeployments` (GET, POST)
- `/mhosts` (GET, POST, PUT)
- `/audit` (GET)

## Automation & Monitoring

- Scripts to automate creation/configuration of deployments and mhosts
- Simulated monitoring: periodic status updates, audit logging

## Frontend

- React app to visualize deployments, subdeployments, mhosts, and audit logs
- Forms to create and configure entities
- Dashboard for monitoring status
