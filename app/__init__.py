#app/__init__.py
from flask import Flask, redirect, render_template, request, current_app, url_for
from flask_restx import Api
from .models.upload import UPLOAD_FOLDER
from .resources.project_resources import ns as project_ns
from .models.upload import allowed_file
from werkzeug.utils import secure_filename
import os
from .models.user import db, User  # Import db and User model
from flask_login import LoginManager
from flask_cors import CORS
from flask_swagger import swagger



def create_app():
    app = Flask(__name__,template_folder='../frontend')
    CORS(app)
    swagger = swagger(app)  
    app.config['SECRET_KEY'] = '9898943'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:9898943@localhost:5432/ec530')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'user_login'  # This must match the endpoint for login
    with app.app_context():
        db.create_all()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    @app.route('/')
    def index():
        # Redirect to the login route
        return redirect(url_for('user_login'))
    api = Api(app)
    api.add_namespace(project_ns)
   
    return app


'''

def create_app():
    app = Flask(__name__,template_folder='../frontend')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9898943@localhost/ec530'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize SQLAlchemy with the app

    @app.route('/')
    def index():
        return render_template('login.html')
    api = Api(app, version='1.0', title='DIY Machine Learning API',
              description='A simple DIY Machine Learning API')
    api.add_namespace(project_ns)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    with app.app_context():
        db.create_all()  # Create tables

    return app
'''
