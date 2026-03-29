from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from app.schemas.flight_schema import query_flight_response_model
from app.schemas.booking_schema import error_response_model
from app.services.passenger_service import PassengerService
from app.utils.pagination import get_pagination_params

passenger_ns = Namespace("passengers", description="Passenger operations")


@passenger_ns.route("")
class PassengerListResource(Resource):

    @jwt_required()
    @passenger_ns.doc(security="Bearer")
    @passenger_ns.response(200, "Passenger list", query_flight_response_model)
    @passenger_ns.response(400, "Validation error", error_response_model)
    @passenger_ns.response(401, "Unauthorized", error_response_model)
    def get(self):
        """
        Get passenger list (paginated)
        """
        page, per_page = get_pagination_params(request.args)

        response, status_code = PassengerService.get_passenger_list(
            request.args,
            page,
            per_page
        )
        return response, status_code