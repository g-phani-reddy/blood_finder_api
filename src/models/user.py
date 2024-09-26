import datetime
from sqlalchemy.dialects.postgresql import UUID


from src.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True)
    email_id = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(
        datetime.timezone.utc))
    blood_group = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    mobile_num = db.Column(db.String(13))
    mobile_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)


    def __init__(self, user_id, email_id, password_hash, blood_group, gender, age, mobile_num):
        self.user_id = user_id
        self.email_id = email_id
        self.password_hash = password_hash
        self.blood_group = blood_group
        self.gender = gender
        self.age = age
        self.mobile_num = mobile_num
    

    def __repr__(self):
        return {
            "user_id": str(self.user_id),
            "email_id": str(self.email_id),
            "blood_group": str(self.blood_group),
            "gender": str(self.gender),
            "age": self.age,
            "mobile_num": str(self.mobile_num),
            "is_active": self.is_active,
            "email_verified": self.email_verified,
            "mobile_verified": self.mobile_verified,
            "created_at": self.created_at
        }
