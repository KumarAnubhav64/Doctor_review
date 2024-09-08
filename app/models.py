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
