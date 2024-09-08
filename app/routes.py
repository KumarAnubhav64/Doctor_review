from flask import Blueprint, request, jsonify, current_app
from app.controllers import ReviewController
from app.models import TokenModel, ReviewModel

review_blueprint = Blueprint('reviews', __name__)

@review_blueprint.before_request
def init_controller():
    token_model = TokenModel(current_app.db)
    review_model = ReviewModel(current_app.db)
    current_app.review_controller = ReviewController(review_model, token_model)

# API to submit a review
@review_blueprint.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.json
    token = data.get('token')
    review_text = data.get('review')
    doctor_id = data.get('doctor_id')

    if not token or not review_text or not doctor_id:
        return jsonify({'message': 'Missing required fields'}), 400

    return current_app.review_controller.submit_review(token, review_text, doctor_id)

# API to generate a token for an authorized patient
@review_blueprint.route('/generate_token', methods=['POST'])
def generate_token():
    data = request.json
    patient_id = data.get('patient_id')

    if not patient_id:
        return jsonify({'message': 'Patient ID is required'}), 400

    return current_app.review_controller.generate_token(patient_id)

# API to view reviews for a specific doctor
@review_blueprint.route('/view_reviews/<doctor_id>', methods=['GET'])
def view_reviews(doctor_id):
    return current_app.review_controller.view_reviews(doctor_id)
from datetime import datetime

class TokenModel:
    def __init__(self, db):
        self.collection = db['tokens']

    def generate_token(self, patient_id):
        token = f"TOK-{patient_id}-{datetime.now().timestamp()}"
        self.collection.insert_one({
            'token': token,
            'patient_id': patient_id,
            'used': False,
            'created_at': datetime.now()
        })
        return token

    def validate_token(self, token):
        return self.collection.find_one({'token': token, 'used': False})

    def mark_token_used(self, token):
        self.collection.update_one({'token': token}, {'$set': {'used': True}})


class ReviewModel:from flask import Blueprint, request, jsonify, current_app
from app.controllers import ReviewController
from app.models import TokenModel, ReviewModel

review_blueprint = Blueprint('reviews', __name__)

@review_blueprint.before_request
def init_controller():
    token_model = TokenModel(current_app.db)
    review_model = ReviewModel(current_app.db)
    current_app.review_controller = ReviewController(review_model, token_model)

# API to submit a review
@review_blueprint.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.json
    token = data.get('token')
    review_text = data.get('review')
    doctor_id = data.get('doctor_id')

    if not token or not review_text or not doctor_id:
        return jsonify({'message': 'Missing required fields'}), 400

    return current_app.review_controller.submit_review(token, review_text, doctor_id)

# API to generate a token for an authorized patient
@review_blueprint.route('/generate_token', methods=['POST'])
def generate_token():
    data = request.json
    patient_id = data.get('patient_id')

    if not patient_id:
        return jsonify({'message': 'Patient ID is required'}), 400

    return current_app.review_controller.generate_token(patient_id)

# API to view reviews for a specific doctor
@review_blueprint.route('/view_reviews/<doctor_id>', methods=['GET'])
def view_reviews(doctor_id):
    return current_app.review_controller.view_reviews(doctor_id)
from datetime import datetime

class TokenModel:
    def __init__(self, db):
        self.collection = db['tokens']

    def generate_token(self, patient_id):
        token = f"TOK-{patient_id}-{datetime.now().timestamp()}"
        self.collection.insert_one({
            'token': token,
            'patient_id': patient_id,
            'used': False,
            'created_at': datetime.now()
        })
        return token

    def validate_token(self, token):
        return self.collection.find_one({'token': token, 'used': False})

    def mark_token_used(self, token):
        self.collection.update_one({'token': token}, {'$set': {'used': True}})


class ReviewModel:
    def __init__(self, db):
        self.collection = db['reviews']

    def submit_review(self, patient_id, doctor_id, review_text):
        review_data = {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'review': review_text,
            'submitted_at': datetime.now()
        }
        self.collection.insert_one(review_data)

    def get_reviews_for_doctor(self, doctor_id):
        return list(self.collection.find({'doctor_id': doctor_id}))
    def __init__(self, db):
        self.collection = db['reviews']

    def submit_review(self, patient_id, doctor_id, review_text):
        review_data = {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'review': review_text,
            'submitted_at': datetime.now()
        }
        self.collection.insert_one(review_data)

    def get_reviews_for_doctor(self, doctor_id):
        return list(self.collection.find({'doctor_id': doctor_id}))
