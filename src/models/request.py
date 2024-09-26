import datetime
from src.extensions import db
from sqlalchemy.dialects.postgresql import UUID


class Request(db.Model):
    __tablename__ = 'requests'

    request_id = db.Column(UUID(as_uuid=True), primary_key=True)
    requestor_id = db.Column(db.UUID(as_uuid=True))
    priority = db.Column(db.String(20))
    blood_group = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    mobile_num = db.Column(db.String(12))
    requested_at = db.Column(db.DateTime, default=datetime.datetime.now(
        datetime.timezone.utc))
    updated_at = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    donor_id = db.Column(db.String(100))
    document = db.Column(db.String(400))

    def __init__(self, request_id,requestor_id, priority, age,
            gender, mobile_num, requested_at, updated_at, status, donor_id, document):
        self.request_id = request_id
        self.requestor_id = requestor_id
        self.priority = priority
        self.age = age
        self.gender = gender
        self.mobile_num = mobile_num
        self.status = status
        self.donor_id = donor_id
        self.document = document
        self.requested_at = requested_at
        self.updated_at = updated_at


    def __repr__(self):
        return {
            "requestor_id": str(self.requestor_id),
            "request_id": str(self.request_id),
            "priority": str(self.priority),
            "age": self.age,
            "gender": str(self.gender),
            "mobile_num": str(self.mobile_num),
            "requested_at": self.requested_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "donor_id": self.donor_id,
            "document": self.document
        }
