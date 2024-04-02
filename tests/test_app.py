import pytest
from app import create_app  # Ensure this import is correct
from app.models.inference import perform_inference
from app.models.train import train_model

# Assuming a fixture for creating a test client exists, or define it as follows:
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

    # Using patch to emulate the enqueue method
def test_submit_inference(mocker,client):
    # Emulating the enqueue method
    mock_enqueue = mocker.patch('app.resources.project_resources.inference_queue.enqueue', return_value=type('Job', (object,), {'id': 'fake_job_id'})())

    projectId = 123  # Example project ID
    # Send a POST request to the submit_inference endpoint
    response = client.post(f"/{projectId}/submit_inference", json={"data": "inference data"})
    
    # Confirms that the request was processed correctly and returns the job_id
    assert response.status_code == 202
    assert response.json == {'job_id': 'fake_job_id'}
    
    # Verify that enqueue is called correctly 
    mock_enqueue.assert_called_once_with(perform_inference, {"data": "inference data"})

def test_submit_training(mocker, client):
        # Similar adjustments for the training submission test
    mock_enqueue = mocker.patch('app.resources.project_resources.training_queue.enqueue', return_value=type('Job', (object,), {'id': 'fake_job_id'})())
        
    projectId = 123  # Example project ID
        # Send a POST request to the submit_training endpoint
    response = client.post(f"/{projectId}/submit_training", json={"data": "training data"})
        
        # Confirm response status and job_id as before
    assert response.status_code == 202
    assert response.json == {'job_id': 'fake_job_id'}
        
    mock_enqueue.assert_called_once_with(train_model, {"data": "training data"})
