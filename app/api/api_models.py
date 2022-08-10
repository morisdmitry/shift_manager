from flask_restx import fields
from app.api import api


shift_model = api.model(
    "Shift",
    {
        "email": fields.String(required=True, example="test@gmail.com"),
        "start": fields.Integer(required=True, example=1659906573),
        "end": fields.Integer(required=True, example=1659906673),
    },
)
