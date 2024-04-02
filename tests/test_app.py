import json
from unittest.mock import patch
from flask_testing import TestCase
from app import create_app
from app.resources.project_resources import ns
from app.models.inference import perform_inference
from app.models.train import train_model

class MyTest(TestCase):

    def create_app(self):
        # Create a Flask app test instance
        app = create_app()
        #print(app.url_map)
        #app.register_blueprint(ns)  # Register API Blueprint
        app.config['TESTING'] = True
        return app

    # Using patch to emulate the enqueue method
    @patch('app.resources.project_resources.inference_queue.enqueue')
    def test_submit_inference(self, mock_enqueue):
        # Emulating the enqueue method
        mock_enqueue.return_value = type('Job', (object,), {'id': 'fake_job_id'})()
        
        # Send a POST request to the submit_inference endpoint
        response = self.client.post("/<int:projectId>/submit_inference", json={"data": "inference data"})
        
        # Confirms that the request was processed correctly and returns the job_id
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {'job_id': 'fake_job_id'})
        
        # Verify that enqueue is called correctly 
        mock_enqueue.assert_called_once_with(perform_inference, {"data": "inference data"})

    # Using patch to emulate the enqueue method
    @patch('app.resources.project_resources.training_queue.enqueue')
    def test_submit_training(self, mock_enqueue):
        # Emulating the enqueue method
        mock_enqueue.return_value = type('Job', (object,), {'id': 'fake_job_id'})()
        
        # Send a POST request to the submit_training endpoint
        response = self.client.post("/<int:projectId>/submit_training", json={"data": "training data"})
        
        # Confirms that the request was processed correctly and returns the job_id
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json, {'job_id': 'fake_job_id'})
        
        # Verify that enqueue is called correctly 
        mock_enqueue.assert_called_once_with(train_model, {"data": "training data"})