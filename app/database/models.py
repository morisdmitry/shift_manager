from datetime import datetime
from app import db

# from sqlalchemy import BigInteger


class BaseModel(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, *periods: tuple[dict, dict]):

        try:
            for period in periods:
                obj = cls(**period)
                db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            obj = getattr(e, "message", str(e))

        return obj


class Timeshits(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    start = db.Column(db.DateTime, default=datetime.now())
    end = db.Column(db.DateTime, default=datetime.now())
