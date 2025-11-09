"""
Deployment Manager Flask API
Serves analytics data from Hive tables for dashboard consumption
Integrates NetOps and 5G Core deployment analytics
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
from functools import wraps
import yaml
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Global Spark session
spark = None

def get_spark():
    """Get or create Spark session"""
    global spark
    if spark is None:
        spark = SparkSession.builder \
            .appName("DeploymentManagerAPI") \
            .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
            .enableHiveSupport() \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
    return spark


def handle_errors(f):
    """Error handling decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': str(e),
                'message': 'An error occurred processing your request'
            }), 500
    return decorated_function


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Deployment Manager API',
        'version': '1.0.0'
    })


# ==================== DEPLOYMENT OVERVIEW ====================

@app.route('/api/deployment-manager/overview', methods=['GET'])
@handle_errors
def get_deployment_overview():
    """
    Get overall deployment health across NetOps and 5G Core
    Combines metrics from both systems
    """
    spark_session = get_spark()
    days = int(request.args.get('days', 7))

    # NetOps deployment metrics
    netops_query = f"""
        SELECT
            COUNT(DISTINCT site_id) as total_sites,
            AVG(success_rate) as avg_deployment_success,
            SUM(failed) as total_failures,
            SUM(total_executions) as total_deployments
        FROM deployment_analytics.ansible_deployment_metrics
        WHERE date >= DATE_SUB(CURRENT_DATE, {days})
    """

    try:
        netops_metrics = spark_session.sql(netops_query).collect()[0].asDict()
    except:
        netops_metrics = {
            'total_sites': 0,
            'avg_deployment_success': 0,
            'total_failures': 0,
            'total_deployments': 0
        }

    # 5G Core metrics
    core5g_query = f"""
        SELECT
            COUNT(DISTINCT site_id) as sites_with_5g,
            AVG(success_rate) as avg_registration_success,
            SUM(total_attempts) as total_registrations
        FROM deployment_analytics.registration_kpis
        WHERE date >= DATE_SUB(CURRENT_DATE, {days})
    """

    try:
        core5g_metrics = spark_session.sql(core5g_query).collect()[0].asDict()
    except:
        core5g_metrics = {
            'sites_with_5g': 0,
            'avg_registration_success': 0,
            'total_registrations': 0
        }

    # Determine overall health
    overall_health = 'HEALTHY'
    if netops_metrics['avg_deployment_success'] and netops_metrics['avg_deployment_success'] < 90:
        overall_health = 'WARNING'
    if netops_metrics['avg_deployment_success'] and netops_metrics['avg_deployment_success'] < 80:
        overall_health = 'CRITICAL'

    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'period_days': days,
        'network_deployments': {
            'total_sites': int(netops_metrics['total_sites'] or 0),
            'avg_success_rate': round(float(netops_metrics['avg_deployment_success'] or 0), 2),
            'total_failures': int(netops_metrics['total_failures'] or 0),
            'total_deployments': int(netops_metrics['total_deployments'] or 0)
        },
        'core5g_deployments': {
            'sites_with_5g': int(core5g_metrics['sites_with_5g'] or 0),
            'avg_registration_success': round(float(core5g_metrics['avg_registration_success'] or 0), 2),
            'total_registrations': int(core5g_metrics['total_registrations'] or 0)
        },
        'overall_health': overall_health
    })


@app.route('/api/deployment-manager/sites/<site_id>', methods=['GET'])
@handle_errors
def get_site_details(site_id):
    """Get detailed metrics for a specific deployment site"""
    spark_session = get_spark()
    days = int(request.args.get('days', 7))

    query = f"""
        SELECT
            d.site_id,
            AVG(d.success_rate) as deployment_success_rate,
            SUM(d.total_executions) as total_deployments,
            SUM(d.failed) as total_failures
        FROM deployment_analytics.ansible_deployment_metrics d
        WHERE d.site_id = '{site_id}'
        AND d.date >= DATE_SUB(CURRENT_DATE, {days})
        GROUP BY d.site_id
    """

    result = spark_session.sql(query).collect()

    if not result:
        return jsonify({'error': 'Site not found'}), 404

    site_data = result[0].asDict()

    # Get 5G Core metrics if available
    core5g_query = f"""
        SELECT
            AVG(success_rate) as registration_success_rate,
            SUM(total_attempts) as total_registrations
        FROM deployment_analytics.registration_kpis
        WHERE site_id = '{site_id}'
        AND date >= DATE_SUB(CURRENT_DATE, {days})
    """

    try:
        core5g_data = spark_session.sql(core5g_query).collect()[0].asDict()
    except:
        core5g_data = {'registration_success_rate': None, 'total_registrations': 0}

    return jsonify({
        'site_id': site_id,
        'netops': {
            'success_rate': round(float(site_data['deployment_success_rate'] or 0), 2),
            'total_deployments': int(site_data['total_deployments'] or 0),
            'total_failures': int(site_data['total_failures'] or 0)
        },
        'core5g': {
            'registration_success_rate': round(float(core5g_data['registration_success_rate'] or 0), 2) if core5g_data['registration_success_rate'] else None,
            'total_registrations': int(core5g_data['total_registrations'] or 0)
        }
    })


# ==================== NETOPS ENDPOINTS ====================

@app.route('/api/netops/deployments', methods=['GET'])
@handle_errors
def get_netops_deployments():
    """Get NetOps deployment statistics"""
    spark_session = get_spark()

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    site_id = request.args.get('site_id')
    playbook = request.args.get('playbook')

    query = "SELECT * FROM deployment_analytics.ansible_deployment_metrics WHERE 1=1"

    if start_date:
        query += f" AND date >= '{start_date}'"
    if end_date:
        query += f" AND date <= '{end_date}'"
    if site_id:
        query += f" AND site_id = '{site_id}'"
    if playbook:
        query += f" AND playbook = '{playbook}'"

    query += " ORDER BY date DESC LIMIT 100"

    df = spark_session.sql(query)
    results = [row.asDict() for row in df.collect()]

    # Convert to JSON-serializable format
    for result in results:
        for key, value in result.items():
            if value is not None and hasattr(value, '__float__'):
                result[key] = float(value)

    return jsonify({
        'total_records': len(results),
        'deployments': results
    })


@app.route('/api/netops/deployment-trends', methods=['GET'])
@handle_errors
def get_deployment_trends():
    """Get deployment trends over time"""
    spark_session = get_spark()
    days = int(request.args.get('days', 30))

    query = f"""
        SELECT
            date,
            playbook,
            total_deployments,
            successful,
            success_rate
        FROM deployment_analytics.daily_deployment_trends
        WHERE date >= DATE_SUB(CURRENT_DATE, {days})
        ORDER BY date ASC
    """

    df = spark_session.sql(query)
    results = [row.asDict() for row in df.collect()]

    return jsonify({
        'period_days': days,
        'trends': results
    })


@app.route('/api/netops/failures', methods=['GET'])
@handle_errors
def get_deployment_failures():
    """Get deployment failures requiring attention"""
    spark_session = get_spark()
    limit = int(request.args.get('limit', 50))

    query = f"""
        SELECT
            playbook,
            error_message,
            site_id,
            failure_count,
            last_failure_date
        FROM deployment_analytics.deployment_failure_analysis
        ORDER BY failure_count DESC
        LIMIT {limit}
    """

    df = spark_session.sql(query)
    results = [row.asDict() for row in df.collect()]

    return jsonify({
        'total_failures': len(results),
        'failures': results
    })


# ==================== 5G CORE ENDPOINTS ====================

@app.route('/api/5g/registration-kpis', methods=['GET'])
@handle_errors
def get_5g_registration_kpis():
    """Get 5G Core registration KPIs"""
    spark_session = get_spark()

    site_id = request.args.get('site_id')
    days = int(request.args.get('days', 7))

    query = f"""
        SELECT
            site_id,
            amf_instance,
            date,
            total_attempts,
            successful,
            success_rate,
            avg_latency,
            deployment_status
        FROM deployment_analytics.registration_kpis
        WHERE date >= DATE_SUB(CURRENT_DATE, {days})
    """

    if site_id:
        query += f" AND site_id = '{site_id}'"

    query += " ORDER BY date DESC"

    df = spark_session.sql(query)
    results = [row.asDict() for row in df.collect()]

    # Calculate summary stats
    if results:
        avg_success = sum(r['success_rate'] for r in results) / len(results)
        critical_sites = [r for r in results if r['deployment_status'] == 'CRITICAL']
    else:
        avg_success = 0
        critical_sites = []

    return jsonify({
        'summary': {
            'total_records': len(results),
            'avg_success_rate': round(avg_success, 2),
            'critical_count': len(critical_sites)
        },
        'kpis': results
    })


@app.route('/api/5g/registration-failures', methods=['GET'])
@handle_errors
def get_5g_registration_failures():
    """Get 5G registration failure analysis"""
    spark_session = get_spark()
    limit = int(request.args.get('limit', 50))

    query = f"""
        SELECT
            failure_reason,
            site_id,
            failure_count
        FROM deployment_analytics.registration_failure_analysis
        ORDER BY failure_count DESC
        LIMIT {limit}
    """

    df = spark_session.sql(query)
    results = [row.asDict() for row in df.collect()]

    return jsonify({
        'total_failure_types': len(results),
        'failures': results
    })


# ==================== STATISTICS ====================

@app.route('/api/stats/summary', methods=['GET'])
@handle_errors
def get_summary_stats():
    """Get summary statistics across all deployments"""
    spark_session = get_spark()
    days = int(request.args.get('days', 7))

    # NetOps stats
    netops_stats_query = f"""
        SELECT
            COUNT(DISTINCT site_id) as total_sites,
            COUNT(DISTINCT playbook) as total_playbooks,
            SUM(total_executions) as total_executions,
            AVG(success_rate) as avg_success_rate
        FROM deployment_analytics.ansible_deployment_metrics
        WHERE date >= DATE_SUB(CURRENT_DATE, {days})
    """

    netops_stats = spark_session.sql(netops_stats_query).collect()[0].asDict()

    # 5G Core stats
    core5g_stats_query = f"""
        SELECT
            COUNT(DISTINCT site_id) as total_5g_sites,
            SUM(total_attempts) as total_registrations,
            AVG(success_rate) as avg_registration_success,
            AVG(avg_latency) as avg_latency
        FROM deployment_analytics.registration_kpis
        WHERE date >= DATE_SUB(CURRENT_DATE, {days})
    """

    try:
        core5g_stats = spark_session.sql(core5g_stats_query).collect()[0].asDict()
    except:
        core5g_stats = {
            'total_5g_sites': 0,
            'total_registrations': 0,
            'avg_registration_success': 0,
            'avg_latency': 0
        }

    return jsonify({
        'period_days': days,
        'netops': {
            'total_sites': int(netops_stats['total_sites'] or 0),
            'total_playbooks': int(netops_stats['total_playbooks'] or 0),
            'total_executions': int(netops_stats['total_executions'] or 0),
            'avg_success_rate': round(float(netops_stats['avg_success_rate'] or 0), 2)
        },
        'core5g': {
            'total_5g_sites': int(core5g_stats['total_5g_sites'] or 0),
            'total_registrations': int(core5g_stats['total_registrations'] or 0),
            'avg_registration_success': round(float(core5g_stats['avg_registration_success'] or 0), 2),
            'avg_latency_ms': round(float(core5g_stats['avg_latency'] or 0), 2)
        }
    })


# ==================== APPLICATION STARTUP ====================

@app.before_request
def before_request():
    """Initialize Spark session before first request"""
    get_spark()


if __name__ == '__main__':
    print("=" * 60)
    print("Starting Deployment Manager API")
    print("=" * 60)
    print("API will be available at: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
