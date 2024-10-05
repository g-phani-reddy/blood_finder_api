import json
from flask import Flask, request, jsonify, Blueprint
from flask.views import MethodView
from src.services import user_services
from src.utilities.verification import token_required, get_token_data, get_token_user

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
            name = data["name"]

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
                blood_group=blood_group,
                name=name
            )
            return {"user_id": str(data)}, 201
        
        except Exception as e:
            return {"message": str(e)}, 500


class UserLogin(MethodView):
    def post(self):
        try:
            data = request.get_json()

            # Validate required fields
            email_id = data['email_id']
            password = data['password']
        except Exception as e:
            print(str(e))
            return {"message": "Bad Request. Invalid input"}, 400
        
        try:
            status, data = user_services.generate_token(
                email_id=email_id, password=password
            )
            if status:
                return {"token": data}, 200
            else:
                return {"message": data}, 400
        except Exception as e:
            return {"message": str(e)}, 500


class UserOperations(MethodView):
    @token_required
    def get(self):
        try:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]
            status, data = get_token_data(token)
            if not status:
                return {"message": str(data)}, 400
            else:
                user_id = data.get("user_id")
                user_data = user_services.get_user_details(
                    user_id=user_id
                )
                return user_data, 200
        except Exception as e:
            return {"message": str(e)}, 500


    @token_required
    def put(self):
        try:
            user_data = get_token_user()
            if not user_data:
                return {"message": "Invalid input"}, 400
            
            request_data = request.get_json()
            update_dict = {}
            update_dict["name"] = request_data.get("name", None)
            update_dict["age"] = request_data.get("age", None)
            update_dict["gender"] = request_data.get("gender", None)
            update_dict["mobile_num"] = request_data.get("mobile_num", None)
            update_dict["blood_group"] = request_data.get("blood_group", None)

            status, data = user_services.update_user(
                user_id=user_data.get('user_id'),
                update_dict=update_dict
            )
            if status:
                return {"message": str(data)}, 200
            else:
                return {"message": str(data)}, 500
        except Exception as e:
            return {"message": str(e)}, 500


class SearchUsers(MethodView):
    @token_required
    def get(self):
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            sort_by = str(request.args.get("sort_by")) if request.args.get(
                "sort_by") else "robot_id"
            sort_order = str(request.args.get("sort_order")) if request.args.get(
                "sort_order") else "desc"

            filters = json.loads(request.args.get("filter")
                    ) if request.args.get("filter") else None
            if sort_order.lower() not in ["asc", "desc"]:
                return {"message": "Invalid sort order"}, 400
            
            users = user_services.search_users(
                per_page=per_page,
                page=page,
                filters=filters,
                sort_by=sort_by, sort_order=sort_order)
            return {"data": users}, 200

        except Exception as err:
            return {"message": str(err)}, 500



signup_view = UserSignUp.as_view('signup_view')
login_view = UserLogin.as_view('login_view')
users_view = UserOperations.as_view('users_view')
search_users_view = SearchUsers.as_view('search_users_view')


user_bp.add_url_rule('/signup', view_func=signup_view, methods=['POST'])
user_bp.add_url_rule('/login', view_func=login_view, methods=['POST'])
user_bp.add_url_rule('/', view_func=users_view, methods=['GET', 'PUT'])
user_bp.add_url_rule('/search', view_func=search_users_view, methods=['GET'])
