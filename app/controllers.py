from flask import jsonify
from bson import ObjectId
import json
from datetime import datetime

def convert_mongo_document(document):
    if '_id' in document:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
    if 'created_at' in document and isinstance(document['created_at'], datetime):
        document['created_at'] = document['created_at'].isoformat()  # Convert datetime to ISO string
    return document


class ReviewController:
    def __init__(self, review_model, token_model):
        self.review_model = review_model
        self.token_model = token_model

    def submit_review(self, token, review_text, doctor_id):
        token_data = self.token_model.validate_token(token)
        if not token_data:
            return jsonify({'message': 'Invalid or used token'}), 400

        # Submit the review
        self.review_model.submit_review(
            patient_id=token_data['patient_id'],
            doctor_id=doctor_id,
            review_text=review_text
        )

        # Mark the token as used
        self.token_model.mark_token_used(token)

        return jsonify({'message': 'Review submitted successfully!'})

    def generate_token(self, patient_id):
        token = self.token_model.generate_token(patient_id)
        return jsonify({'token': token})

    def view_reviews(self, doctor_id):
        reviews = self.review_model.get_reviews_for_doctor(doctor_id)

        if reviews:
        # Convert ObjectId and datetime before passing to jsonify
            l = []
            for review in reviews:

                l.append(convert_mongo_document(review))

            return jsonify(l)
        else:
            return jsonify({'error': 'No data found'})

