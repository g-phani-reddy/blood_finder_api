import uuid
from werkzeug.security import generate_password_hash
from src.models.user import User
from src.extensions import db

def create_user(email_id, password, mobile_num, age, blood_group, gender):
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
            blood_group=blood_group)
        db.session.flush()
        db.session.add(user)
        db.session.commit()
        return True, str(user.user_id)

    except Exception as e:
        db.session.rollback()
        raise Exception(str(e))
