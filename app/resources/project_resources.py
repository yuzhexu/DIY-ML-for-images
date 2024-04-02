from flask import jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from redis import Redis
from rq import Queue
from app.models.inference import perform_inference  
from app.models.train import train_model  

# initial redis connection 
redis_conn = Redis(host='localhost', port=6379, db=0)
# queues
training_queue = Queue('training_tasks', connection=redis_conn)
inference_queue = Queue('inference_tasks', connection=redis_conn)

ns = Namespace('projects', description='Project operations')

upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, action='append', help='One or more image files.')

label_model = ns.model('Label', {
    'imageName': fields.String(required=True, description='The image name'),
    'label': fields.String(required=True, description='The label of the image')
})

training_config_model = ns.model('TrainingConfig', {
    'epochs': fields.Integer(required=True, description='Number of epochs'),
    'batchSize': fields.Integer(required=True, description='Batch size'),
    'learningRate': fields.Float(required=True, description='Learning rate')
})

@ns.route('/<int:projectId>/images/upload')
@ns.expect(upload_parser)
class ImageUpload(Resource):
    @ns.doc(description='Allows users to upload images for a specific project. The endpoint supports uploading multiple images in one request.')
    def post(self, projectId):
        # Implementing Upload Logic
        return {'success': True, 'message': 'Images uploaded successfully'}, 200

@ns.route('/<int:projectId>/labels/upload')
@ns.expect(label_model)
class LabelUpload(Resource):
    @ns.doc(description='Uploads label or class data for the images in a specific project.')
    def post(self, projectId):
        # Implementing label upload logic
        return {'success': True, 'message': 'Labels uploaded successfully'}, 200

@ns.route('/<int:projectId>/analyze')
class DataAnalyze(Resource):
    @ns.doc(description='Analyzes uploaded data to provide insights before training.')
    def get(self, projectId):
        # Implementing data analysis logic
        return {'success': True, 'data': {'analysisResults': 'Some results'}}, 200

@ns.route('/<int:projectId>/training/configure')
@ns.expect(training_config_model)
class TrainingConfigure(Resource):
    @ns.doc(description='Allows users to configure training parameters for a machine learning model.')
    def post(self, projectId):
        # Implement training parameter configuration logic
        return {'success': True, 'message': 'Training configured successfully'}, 200


@ns.route('/<int:projectId>/submit_inference', methods=['POST'])
class submit_inference(Resource):
    def post(self):
       data = request.get_json()
       job = inference_queue.enqueue(perform_inference, data)
       return jsonify({'job_id': job.id}), 202

@ns.route('/<int:projectId>/submit_training', methods=['POST'])
class submit_training(Resource):
    def post(self):
        data = request.get_json()
        job = training_queue.enqueue(train_model, data)
        return jsonify({'job_id': job.id}), 202