from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from app.schemas.booking_schema import (
    buy_ticket_request_model,
    buy_ticket_response_model,
    error_response_model
)
from app.services.booking_service import BookingService

booking_ns = Namespace("bookings", description="Booking operations")


@booking_ns.route("")
class BookingResource(Resource):

    @jwt_required()
    @booking_ns.doc(security="Bearer")
    @booking_ns.expect(buy_ticket_request_model, validate=True)
    @booking_ns.response(201, "Ticket purchased", buy_ticket_response_model)
    @booking_ns.response(400, "Validation error", error_response_model)
    @booking_ns.response(401, "Unauthorized", error_response_model)
    @booking_ns.response(404, "Flight not found", error_response_model)
    def post(self):
        """
        Buy a ticket
        """
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}

        response, status_code = BookingService.buy_ticket(data, user_id)
        return response, status_code