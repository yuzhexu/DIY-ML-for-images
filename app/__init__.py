from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='DIY Machine Learning API',
              description='A simple DIY Machine Learning API')

    from .resources.project_resources import ns as project_ns
    api.add_namespace(project_ns)

    # 如果有其他命名空间，继续在这里添加

    return app

