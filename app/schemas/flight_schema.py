from flask_restx import fields

from app import api

add_flight_request_model = api.model(
    "AddFlightRequest",
    {
        "flight_number": fields.String(required=True, description="Flight number"),
        "date_from": fields.String(required=True, description="Departure datetime in ISO format"),
        "date_to": fields.String(required=True, description="Arrival datetime in ISO format"),
        "airport_from": fields.String(required=True, description="Departure airport code"),
        "airport_to": fields.String(required=True, description="Arrival airport code"),
        "duration": fields.Integer(required=True, description="Duration in minutes"),
        "capacity": fields.Integer(required=True, description="Flight capacity")
    }
)

flight_response_model = api.model(
    "FlightResponse",
    {
        "id": fields.Integer,
        "flight_number": fields.String,
        "date_from": fields.String,
        "date_to": fields.String,
        "airport_from": fields.String,
        "airport_to": fields.String,
        "duration": fields.Integer,
        "capacity": fields.Integer,
        "available_seats": fields.Integer,
        "created_at": fields.String
    }
)

add_flight_success_response_model = api.model(
    "AddFlightSuccessResponse",
    {
        "status": fields.String,
        "message": fields.String,
        "data": fields.Raw
    }
)

upload_flights_response_model = api.model(
    "UploadFlightsResponse",
    {
        "status": fields.String,
        "message": fields.String,
        "data": fields.Raw
    }
)

flight_search_item_model = api.model(
    "FlightSearchItem",
    {
        "flight_number": fields.String,
        "date_from": fields.String,
        "date_to": fields.String,
        "airport_from": fields.String,
        "airport_to": fields.String,
        "duration": fields.Integer,
        "available_seats": fields.Integer
    }
)

query_flight_response_model = api.model(
    "QueryFlightResponse",
    {
        "status": fields.String,
        "message": fields.String,
        "page": fields.Integer,
        "per_page": fields.Integer,
        "total": fields.Integer,
        "pages": fields.Integer,
        "data": fields.List(fields.Raw)
    }
)

error_response_model = api.model(
    "FlightErrorResponse",
    {
        "status": fields.String,
        "message": fields.String
    }
)