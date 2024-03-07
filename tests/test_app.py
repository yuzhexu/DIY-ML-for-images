import pytest
from flask_testing import TestCase
from app import create_app  

class MyTest(TestCase):

    def create_app(self):
        # create Flask app instance for testing
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_home(self):
        # Send an HTTP GET request to the root route and validate the response
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        


