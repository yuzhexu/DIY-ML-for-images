#app/resources/project_resources.py
from flask import Response, json, jsonify, make_response, redirect, request, current_app, render_template, send_from_directory, url_for
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from redis import Redis
from rq import Queue
from app.models.inference import perform_inference  
from app.models.train import train_model  
from app.models.upload import allowed_file
from app.models.user import User, db 
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io
from flask_login import login_user, logout_user, login_required



# initial redis connection 
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')  # 使用 REDIS_URL 环境变量
redis_conn = Redis.from_url(redis_url)

# queues
training_queue = Queue('submit_training', connection=redis_conn)
inference_queue = Queue('submit_inference', connection=redis_conn)

ns = Namespace('projects', path='/api', description='Project operations')
user_model = ns.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', type=FileStorage, location='files', required=True, help='Image file to upload.')

@ns.route('/index', endpoint='index_main')
class index(Resource):
    def get(self):
            @login_required
            def protected():
                html_content = render_template('index.html')
                response = make_response(html_content)
                response.headers['Content-Type'] = 'text/html'
                return response
            return protected()
        

@ns.route('/register')
class UserRegister(Resource):
    def get(self):
        html_content = render_template('register.html')
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        return response
    
    @ns.expect(user_model)
    def post(self):
        data = ns.payload

        user = User(username=data['username'], email=data['email'])

        user.set_password(data['password'])


        if user.passwordhash is None:
            message = json.dumps({'error': 'Failed to generate password hash'})
            return Response(message, status=500, mimetype='application/json')

        db.session.add(user)
        try:
            db.session.commit()
            message = json.dumps({'message': 'User registered successfully'})
            return Response(message, status=201, mimetype='application/json')
        except Exception as e:
            db.session.rollback()
            message = json.dumps({'error': 'Database commit failed'})
            return Response(message, status=500, mimetype='application/json')


@ns.route('/login', endpoint='user_login')
class UserLogin(Resource):
    def get(self):
        html_content = render_template('login.html')
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        return response

    @ns.expect(user_model, validate=True)
    def post(self):
            print("Received POST request")

            try:
                data = request.get_json(force=True)
                print("Data received:", data)

                if not data:
                    message = json.dumps({'message': 'No data received'})
                    return Response(message, status=400, mimetype='application/json')

                print("Looking up user")
                user = User.query.filter_by(username=data['username']).first()
                print("User found:", user)
                if user and user.check_password(data['password']):
                    print("Password is correct")
                    login_user(user, remember=True)
                    response = jsonify({'redirect': url_for('index_main')})
                    response.status_code = 200
                    return response

                else:
                    print("Invalid username or password")
                    message = json.dumps({'error': 'Invalid username or password'})
                    return Response(message, status=401, mimetype='application/json')

            except Exception as e:
                print("Error:", str(e))
                message = json.dumps({'error': 'Server error', 'details': str(e)}), 500
                return Response(message, status=500, mimetype='application/json')

@ns.route('/logout')
class UserLogout(Resource):
    @login_required
    def post(self):
        logout_user()
        response = jsonify({'redirect': url_for('user_login')})
        response.status_code = 200
        return response
@ns.route('/uploadDateset')
class Upload(Resource):  # 继承自 Resource
    def post(self):
        # 检查请求中是否有文件部分
        if 'file' not in request.files:
            message = json.dumps({'message': 'No file part'})
            return Response(message, status=400, mimetype='application/json')
        file = request.files['file']
        # 检查文件名是否为空
        if file.filename == '':
            message = json.dumps({'message': 'No selected file'})
            return Response(message, status=400, mimetype='application/json')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            message = json.dumps({'message': 'File uploaded successfully'})
            return Response(message, status=201, mimetype='application/json')
        message = json.dumps({'message': 'Invalid file type'})
        return Response(message, status=400, mimetype='application/json')

@ns.route('/submit_inference', methods=['POST'])
class submit_inference(Resource):
    @ns.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        image_file = args['file']
        if image_file:
            image = Image.open(io.BytesIO(image_file.read()))
            label = perform_inference(image)
            message = json.dumps({'label': label})
            return Response(message, status=200, mimetype='application/json')

        message = json.dumps({'message': 'No file found or invalid image format'})
        return Response(message, status=400, mimetype='application/json')

@ns.route('/submit_training', methods=['POST'])
class submit_training(Resource):
    def post(self):
        data = request.get_json()
        job = training_queue.enqueue(train_model, data)
        message = json.dumps({'job_id': job.id}), 202
        return Response(message, status=202, mimetype='application/json')

