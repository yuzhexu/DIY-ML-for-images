from flask import Flask
from flask_restx import Api
from .resources.project_resources import ns as project_ns


def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='DIY Machine Learning API',
              description='A simple DIY Machine Learning API')
    api.add_namespace(project_ns)

    

    return app

