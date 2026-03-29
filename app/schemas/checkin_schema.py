from flask_restx import fields
from app import api

checkin_request_model = api.model(
    "CheckInRequest",
    {
        "flight_number": fields.String(required=True),
        "date": fields.String(required=True, description="YYYY-MM-DD"),
        "passenger_name": fields.String(required=True)
    }
)

checkin_response_model = api.model(
    "CheckInResponse",
    {
        "status": fields.String,
        "message": fields.String,
        "seat_number": fields.String
    }
)

error_response_model = api.model(
    "CheckInErrorResponse",
    {
        "status": fields.String,
        "message": fields.String
    }
)