
from flask import Flask, request, jsonify, Blueprint
from flask.views import MethodView
from src.services import user_services

user_bp = Blueprint('user', __name__)

class UserSignUp(MethodView):
    def post(self):
        try:
            data = request.get_json()

            # Validate required fields
            email_id = data["email_id"]
            password = data["password"]
            mobile_num = data["mobile_num"]
            age = data["age"]
            gender = data["gender"]
            blood_group = data["blood_group"]

        except Exception as e:
            print(str(e))
            return {"message": "Bad Request. Invalid input"}, 400
        
        try:
            status, data = user_services.create_user(
                email_id=email_id,
                password=password,
                mobile_num=mobile_num,
                age=age,
                gender=gender,
                blood_group=blood_group
            )
            return {"user_id": str(data)}, 201
        
        except Exception as e:
            return {"message": str(e)}, 500


signup_view = UserSignUp.as_view('signup_view')
user_bp.add_url_rule('/signup', view_func=signup_view, methods=['POST'])
