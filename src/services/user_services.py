import uuid, os
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User
from src.extensions import db
from sqlalchemy import desc, asc

def create_user(email_id, password, mobile_num, age, blood_group, gender, name):
    try:
        password_hash = generate_password_hash(password)
        user_id = str(uuid.uuid4())
        user = User(
            user_id=user_id,
            email_id=email_id,
            password_hash=password_hash,
            mobile_num=mobile_num,
            gender=gender,
            age=age,
            blood_group=blood_group,
            name=name)
        db.session.flush()
        db.session.add(user)
        db.session.commit()
        return True, str(user.user_id)

    except Exception as e:
        db.session.rollback()
        raise Exception(str(e))


def generate_token(email_id, password):
    try:
        user = User.query.filter_by(email_id=email_id).first()
        
        if user is None:
            return False, "User not found"

        if not check_password_hash(user.password_hash, password):
            return False, "Invalid password"
        
        token_data = {
            'user_id': str(user.user_id),
            'email': str(user.email_id),
            'exp': (datetime.datetime.now(datetime.timezone.utc)
                     + datetime.timedelta(hours=1)),
            'iat': datetime.datetime.now(datetime.timezone.utc),
        }
        token = jwt.encode(token_data, os.getenv("SECRET_KEY"), algorithm="HS256")
        
        return True, token
    
    except Exception as e:
        return False, str(e)


def get_user_details(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {}
        else:
            return user.__repr__()
    except Exception as e:
        raise Exception(str(e))


def update_user(user_id, update_dict):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return False, "user not found"
        else:
            for attribute in update_dict:
                if update_dict[attribute] is not None:
                    setattr(user, attribute, update_dict[attribute])
            db.session.flush()
            db.session.commit()
            return True, "successfully updated user"
    except Exception as e:
        return False, str(e)


def fomat_users(paginated_users):
    try:
        result = []
        for user in paginated_users:
            result.append({
                "user_id": str(user.user_id),
                "name": str(user.name),
                "email": str(user.email_id),
                "age": str(user.age),
                "gender": str(user.gender),
                "mobile_verified": user.mobile_verified,
                "email_verified": user.email_verified,
                "mobile_num": str(user.mobile_num)
            })
        return result
    except:
        return []


def search_users(per_page, page, filters, sort_by, sort_order):
    try:
        query = User.query

        if filters:
            for column_name, value in filters.items():
                if value is not None: 
                    column = getattr(User, column_name, None)
                    if column:
                        if isinstance(value, str) and hasattr(column.property.columns[0].type, 'length'):
                            query = query.filter(column.ilike(f'%{value}%'))
                        else:
                            query = query.filter(column == value)

        sort_column = getattr(User, sort_by, None)
        if sort_column:
            if sort_order == 'desc':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

        paginated_users = query.paginate(page=page, per_page=per_page, error_out=False)
        result = fomat_users(paginated_users)
        return result
    except Exception as e:
        print(str(e))
        return []
