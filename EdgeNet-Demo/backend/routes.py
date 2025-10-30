from flask import Blueprint, request, jsonify
from models import db, Deployment, Subdeployment, Mhost, AuditLog
from sqlalchemy.exc import IntegrityError
import json

api_bp = Blueprint('api', __name__)

def log_audit(entity_type, entity_id, action, details=None):
    audit_log = AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        details=details
    )
    db.session.add(audit_log)
    db.session.commit()

@api_bp.route('/deployments', methods=['GET'])
def get_deployments():
    deployments = Deployment.query.all()
    return jsonify([d.to_dict() for d in deployments]), 200

@api_bp.route('/deployments', methods=['POST'])
def create_deployment():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    try:
        deployment = Deployment(
            name=data['name'],
            status=data.get('status', 'pending')
        )
        db.session.add(deployment)
        db.session.commit()

        log_audit('deployment', deployment.id, 'created', f"Created deployment: {deployment.name}")

        return jsonify(deployment.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Deployment with this name already exists'}), 409

@api_bp.route('/deployments/<int:deployment_id>', methods=['GET'])
def get_deployment(deployment_id):
    deployment = Deployment.query.get_or_404(deployment_id)
    return jsonify(deployment.to_dict()), 200

@api_bp.route('/deployments/<int:deployment_id>', methods=['PUT'])
def update_deployment(deployment_id):
    deployment = Deployment.query.get_or_404(deployment_id)
    data = request.get_json()

    if 'status' in data:
        deployment.status = data['status']
    if 'name' in data:
        deployment.name = data['name']

    db.session.commit()
    log_audit('deployment', deployment.id, 'updated', f"Updated deployment: {deployment.name}")

    return jsonify(deployment.to_dict()), 200

@api_bp.route('/deployments/<int:deployment_id>', methods=['DELETE'])
def delete_deployment(deployment_id):
    deployment = Deployment.query.get_or_404(deployment_id)
    deployment_name = deployment.name

    db.session.delete(deployment)
    db.session.commit()

    log_audit('deployment', deployment_id, 'deleted', f"Deleted deployment: {deployment_name}")

    return jsonify({'message': 'Deployment deleted successfully'}), 200

@api_bp.route('/subdeployments', methods=['GET'])
def get_subdeployments():
    deployment_id = request.args.get('deployment_id', type=int)

    if deployment_id:
        subdeployments = Subdeployment.query.filter_by(deployment_id=deployment_id).all()
    else:
        subdeployments = Subdeployment.query.all()

    return jsonify([sd.to_dict() for sd in subdeployments]), 200

@api_bp.route('/subdeployments', methods=['POST'])
def create_subdeployment():
    data = request.get_json()

    if not data or 'name' not in data or 'deployment_id' not in data:
        return jsonify({'error': 'Name and deployment_id are required'}), 400

    deployment = Deployment.query.get(data['deployment_id'])
    if not deployment:
        return jsonify({'error': 'Deployment not found'}), 404

    subdeployment = Subdeployment(
        name=data['name'],
        deployment_id=data['deployment_id'],
        status=data.get('status', 'pending')
    )
    db.session.add(subdeployment)
    db.session.commit()

    log_audit('subdeployment', subdeployment.id, 'created', f"Created subdeployment: {subdeployment.name}")

    return jsonify(subdeployment.to_dict()), 201

@api_bp.route('/subdeployments/<int:subdeployment_id>', methods=['PUT'])
def update_subdeployment(subdeployment_id):
    subdeployment = Subdeployment.query.get_or_404(subdeployment_id)
    data = request.get_json()

    if 'status' in data:
        subdeployment.status = data['status']
    if 'name' in data:
        subdeployment.name = data['name']

    db.session.commit()
    log_audit('subdeployment', subdeployment.id, 'updated', f"Updated subdeployment: {subdeployment.name}")

    return jsonify(subdeployment.to_dict()), 200

@api_bp.route('/subdeployments/<int:subdeployment_id>', methods=['DELETE'])
def delete_subdeployment(subdeployment_id):
    subdeployment = Subdeployment.query.get_or_404(subdeployment_id)
    subdeployment_name = subdeployment.name

    db.session.delete(subdeployment)
    db.session.commit()

    log_audit('subdeployment', subdeployment_id, 'deleted', f"Deleted subdeployment: {subdeployment_name}")

    return jsonify({'message': 'Subdeployment deleted successfully'}), 200

@api_bp.route('/mhosts', methods=['GET'])
def get_mhosts():
    subdeployment_id = request.args.get('subdeployment_id', type=int)

    if subdeployment_id:
        mhosts = Mhost.query.filter_by(subdeployment_id=subdeployment_id).all()
    else:
        mhosts = Mhost.query.all()

    return jsonify([mh.to_dict() for mh in mhosts]), 200

@api_bp.route('/mhosts', methods=['POST'])
def create_mhost():
    data = request.get_json()

    if not data or 'hostname' not in data or 'subdeployment_id' not in data:
        return jsonify({'error': 'Hostname and subdeployment_id are required'}), 400

    subdeployment = Subdeployment.query.get(data['subdeployment_id'])
    if not subdeployment:
        return jsonify({'error': 'Subdeployment not found'}), 404

    try:
        mhost = Mhost(
            hostname=data['hostname'],
            subdeployment_id=data['subdeployment_id'],
            config=data.get('config', '{}'),
            status=data.get('status', 'offline')
        )
        db.session.add(mhost)
        db.session.commit()

        log_audit('mhost', mhost.id, 'created', f"Created mhost: {mhost.hostname}")

        return jsonify(mhost.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Mhost with this hostname already exists'}), 409

@api_bp.route('/mhosts/<int:mhost_id>', methods=['PUT'])
def update_mhost(mhost_id):
    mhost = Mhost.query.get_or_404(mhost_id)
    data = request.get_json()

    if 'status' in data:
        mhost.status = data['status']
    if 'config' in data:
        mhost.config = data['config'] if isinstance(data['config'], str) else json.dumps(data['config'])
    if 'hostname' in data:
        mhost.hostname = data['hostname']

    db.session.commit()
    log_audit('mhost', mhost.id, 'updated', f"Updated mhost: {mhost.hostname}")

    return jsonify(mhost.to_dict()), 200

@api_bp.route('/mhosts/<int:mhost_id>', methods=['DELETE'])
def delete_mhost(mhost_id):
    mhost = Mhost.query.get_or_404(mhost_id)
    mhost_hostname = mhost.hostname

    db.session.delete(mhost)
    db.session.commit()

    log_audit('mhost', mhost_id, 'deleted', f"Deleted mhost: {mhost_hostname}")

    return jsonify({'message': 'Mhost deleted successfully'}), 200

@api_bp.route('/audit', methods=['GET'])
def get_audit_logs():
    entity_type = request.args.get('entity_type')
    entity_id = request.args.get('entity_id', type=int)
    limit = request.args.get('limit', default=100, type=int)

    query = AuditLog.query

    if entity_type:
        query = query.filter_by(entity_type=entity_type)
    if entity_id:
        query = query.filter_by(entity_id=entity_id)

    audit_logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()

    return jsonify([log.to_dict() for log in audit_logs]), 200

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        'total_deployments': Deployment.query.count(),
        'total_subdeployments': Subdeployment.query.count(),
        'total_mhosts': Mhost.query.count(),
        'active_mhosts': Mhost.query.filter_by(status='online').count(),
        'offline_mhosts': Mhost.query.filter_by(status='offline').count()
    }

    return jsonify(stats), 200
