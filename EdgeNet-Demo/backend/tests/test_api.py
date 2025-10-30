import unittest
import json
from app import create_app
from models import db, Deployment, Subdeployment, Mhost, AuditLog

class EdgeNetAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_deployment(self):
        response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Test-Deployment', 'status': 'active'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test-Deployment')
        self.assertEqual(data['status'], 'active')

    def test_get_deployments(self):
        self.client.post('/api/deployments',
            data=json.dumps({'name': 'Deployment1'}),
            content_type='application/json'
        )
        self.client.post('/api/deployments',
            data=json.dumps({'name': 'Deployment2'}),
            content_type='application/json'
        )

        response = self.client.get('/api/deployments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_create_deployment_duplicate_name(self):
        self.client.post('/api/deployments',
            data=json.dumps({'name': 'Duplicate'}),
            content_type='application/json'
        )

        response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Duplicate'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_update_deployment(self):
        create_response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Test-Deployment'}),
            content_type='application/json'
        )
        deployment_id = json.loads(create_response.data)['id']

        response = self.client.put(f'/api/deployments/{deployment_id}',
            data=json.dumps({'status': 'inactive'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'inactive')

    def test_delete_deployment(self):
        create_response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Test-Deployment'}),
            content_type='application/json'
        )
        deployment_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/api/deployments/{deployment_id}')
        self.assertEqual(response.status_code, 200)

        get_response = self.client.get('/api/deployments')
        data = json.loads(get_response.data)
        self.assertEqual(len(data), 0)

    def test_create_subdeployment(self):
        deployment_response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Parent-Deployment'}),
            content_type='application/json'
        )
        deployment_id = json.loads(deployment_response.data)['id']

        response = self.client.post('/api/subdeployments',
            data=json.dumps({
                'name': 'Sub-Deployment',
                'deployment_id': deployment_id
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Sub-Deployment')
        self.assertEqual(data['deployment_id'], deployment_id)

    def test_create_subdeployment_invalid_deployment(self):
        response = self.client.post('/api/subdeployments',
            data=json.dumps({
                'name': 'Sub-Deployment',
                'deployment_id': 9999
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_create_mhost(self):
        deployment_response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Parent-Deployment'}),
            content_type='application/json'
        )
        deployment_id = json.loads(deployment_response.data)['id']

        subdep_response = self.client.post('/api/subdeployments',
            data=json.dumps({
                'name': 'Sub-Deployment',
                'deployment_id': deployment_id
            }),
            content_type='application/json'
        )
        subdep_id = json.loads(subdep_response.data)['id']

        response = self.client.post('/api/mhosts',
            data=json.dumps({
                'hostname': 'test-host.example.com',
                'subdeployment_id': subdep_id,
                'status': 'online'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['hostname'], 'test-host.example.com')
        self.assertEqual(data['status'], 'online')

    def test_update_mhost_status(self):
        deployment_response = self.client.post('/api/deployments',
            data=json.dumps({'name': 'Parent-Deployment'}),
            content_type='application/json'
        )
        deployment_id = json.loads(deployment_response.data)['id']

        subdep_response = self.client.post('/api/subdeployments',
            data=json.dumps({
                'name': 'Sub-Deployment',
                'deployment_id': deployment_id
            }),
            content_type='application/json'
        )
        subdep_id = json.loads(subdep_response.data)['id']

        mhost_response = self.client.post('/api/mhosts',
            data=json.dumps({
                'hostname': 'test-host.example.com',
                'subdeployment_id': subdep_id
            }),
            content_type='application/json'
        )
        mhost_id = json.loads(mhost_response.data)['id']

        response = self.client.put(f'/api/mhosts/{mhost_id}',
            data=json.dumps({'status': 'online'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'online')

    def test_get_audit_logs(self):
        self.client.post('/api/deployments',
            data=json.dumps({'name': 'Test-Deployment'}),
            content_type='application/json'
        )

        response = self.client.get('/api/audit')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['entity_type'], 'deployment')
        self.assertEqual(data[0]['action'], 'created')

    def test_get_stats(self):
        self.client.post('/api/deployments',
            data=json.dumps({'name': 'Test-Deployment'}),
            content_type='application/json'
        )

        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_deployments'], 1)
        self.assertEqual(data['total_subdeployments'], 0)
        self.assertEqual(data['total_mhosts'], 0)

if __name__ == '__main__':
    unittest.main()
