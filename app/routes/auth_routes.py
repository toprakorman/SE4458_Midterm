from flask import request
from flask_restx import Namespace, Resource

from app.schemas.auth_schema import (
    register_request_model,
    login_request_model,
    register_success_response_model,
    auth_success_response_model,
    error_response_model
)
from app.services.auth_service import AuthService

auth_ns = Namespace("auth", description="Authentication operations")


@auth_ns.route("/register")
class RegisterResource(Resource):
    @auth_ns.expect(register_request_model, validate=True)
    @auth_ns.response(201, "User registered successfully", register_success_response_model)
    @auth_ns.response(400, "Validation error", error_response_model)
    @auth_ns.response(409, "Conflict", error_response_model)
    def post(self):
        """
        Register a new user
        """
        data = request.get_json() or {}
        response, status_code = AuthService.register_user(data)
        return response, status_code


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_request_model, validate=True)
    @auth_ns.response(200, "Login successful", auth_success_response_model)
    @auth_ns.response(400, "Validation error", error_response_model)
    @auth_ns.response(401, "Unauthorized", error_response_model)
    def post(self):
        """
        Login and get JWT token
        """
        data = request.get_json() or {}
        response, status_code = AuthService.login_user(data)
        return response, status_code