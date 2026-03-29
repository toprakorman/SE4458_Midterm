from flask_restx import fields
from app import api

buy_ticket_request_model = api.model(
    "BuyTicketRequest",
    {
        "flight_number": fields.String(required=True),
        "date": fields.String(required=True, description="YYYY-MM-DD"),
        "passenger_names": fields.List(
            fields.String,
            required=True,
            description="List of passenger names"
        ),
        "trip_type": fields.String(default="one_way")
    }
)

buy_ticket_response_model = api.model(
    "BuyTicketResponse",
    {
        "status": fields.String,
        "message": fields.String,
        "ticket_number": fields.String
    }
)

error_response_model = api.model(
    "BookingErrorResponse",
    {
        "status": fields.String,
        "message": fields.String
    }
)