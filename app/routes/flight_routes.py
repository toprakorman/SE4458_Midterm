from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restx import Namespace, Resource

from app.extensions import limiter
from app.schemas.flight_schema import (
    add_flight_request_model,
    add_flight_success_response_model,
    upload_flights_response_model,
    query_flight_response_model,
    error_response_model
)
from app.services.flight_service import FlightService
from app.services.file_import_service import FileImportService
from app.utils.pagination import get_pagination_params
from app.utils.response_helpers import error_response

flight_ns = Namespace("flights", description="Flight operations")


@flight_ns.route("")
class FlightCreateResource(Resource):
    @jwt_required()
    @flight_ns.doc(security="Bearer")
    @flight_ns.expect(add_flight_request_model, validate=True)
    @flight_ns.response(201, "Flight added successfully", add_flight_success_response_model)
    @flight_ns.response(400, "Validation error", error_response_model)
    @flight_ns.response(401, "Unauthorized", error_response_model)
    @flight_ns.response(403, "Forbidden", error_response_model)
    @flight_ns.response(409, "Conflict", error_response_model)
    def post(self):
        claims = get_jwt()
        user_role = claims.get("role")

        if user_role != "admin":
            return error_response("Only admin users can add flights"), 403

        data = request.get_json() or {}
        response, status_code = FlightService.add_flight(data)
        return response, status_code


@flight_ns.route("/upload")
class FlightUploadResource(Resource):
    @jwt_required()
    @flight_ns.doc(
        security="Bearer",
        consumes=["multipart/form-data"],
        params={
            "file": {
                "in": "formData",
                "type": "file",
                "required": True,
                "description": "CSV file containing flights"
            }
        }
    )
    @flight_ns.response(200, "File processed successfully", upload_flights_response_model)
    @flight_ns.response(400, "Validation error", error_response_model)
    @flight_ns.response(401, "Unauthorized", error_response_model)
    @flight_ns.response(403, "Forbidden", error_response_model)
    def post(self):
        claims = get_jwt()
        user_role = claims.get("role")

        if user_role != "admin":
            return error_response("Only admin users can upload flights"), 403

        if "file" not in request.files:
            return error_response("CSV file is required with form-data key 'file'"), 400

        file_storage = request.files["file"]
        response, status_code = FileImportService.import_flights_from_csv(file_storage)
        return response, status_code


@flight_ns.route("/search")
class FlightSearchResource(Resource):
    @limiter.limit("3 per day")
    @flight_ns.response(200, "Flights fetched successfully", query_flight_response_model)
    @flight_ns.response(400, "Validation error", error_response_model)
    @flight_ns.response(429, "Rate limit exceeded", error_response_model)
    def get(self):
        page, per_page = get_pagination_params(request.args)
        response, status_code = FlightService.search_flights(
            request.args,
            page,
            per_page
        )
        return response, status_code