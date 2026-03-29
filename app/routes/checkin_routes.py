from flask import request
from flask_restx import Namespace, Resource

from app.schemas.checkin_schema import (
    checkin_request_model,
    checkin_response_model,
    error_response_model
)
from app.services.checkin_service import CheckInService

checkin_ns = Namespace("checkin", description="Check-in operations")


@checkin_ns.route("")
class CheckInResource(Resource):

    @checkin_ns.expect(checkin_request_model, validate=True)
    @checkin_ns.response(200, "Check-in successful", checkin_response_model)
    @checkin_ns.response(400, "Validation error", error_response_model)
    @checkin_ns.response(404, "Not found", error_response_model)
    def post(self):
        """
        Check-in passenger
        (NO AUTH required per assignment)
        """
        data = request.get_json() or {}
        response, status_code = CheckInService.check_in(data)
        return response, status_code