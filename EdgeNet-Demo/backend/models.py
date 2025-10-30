from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Deployment(db.Model):
    __tablename__ = 'deployments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subdeployments = db.relationship('Subdeployment', backref='deployment', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'subdeployments': [sd.to_dict() for sd in self.subdeployments]
        }

class Subdeployment(db.Model):
    __tablename__ = 'subdeployments'

    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mhosts = db.relationship('Mhost', backref='subdeployment', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'deployment_id': self.deployment_id,
            'name': self.name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'mhosts': [mh.to_dict() for mh in self.mhosts]
        }

class Mhost(db.Model):
    __tablename__ = 'mhosts'

    id = db.Column(db.Integer, primary_key=True)
    subdeployment_id = db.Column(db.Integer, db.ForeignKey('subdeployments.id'), nullable=False)
    hostname = db.Column(db.String(100), nullable=False, unique=True)
    config = db.Column(db.Text, default='{}')
    status = db.Column(db.String(50), default='offline')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'subdeployment_id': self.subdeployment_id,
            'hostname': self.hostname,
            'config': self.config,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
