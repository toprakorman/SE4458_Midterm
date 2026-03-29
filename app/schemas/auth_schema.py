from flask_restx import fields

from app import api

register_request_model = api.model(
    "RegisterRequest",
    {
        "username": fields.String(required=True, description="Unique username"),
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
        "role": fields.String(
            required=False,
            description="User role (admin or customer)",
            default="customer"
        )
    }
)

login_request_model = api.model(
    "LoginRequest",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password")
    }
)

auth_success_response_model = api.model(
    "AuthSuccessResponse",
    {
        "status": fields.String(description="Operation status"),
        "message": fields.String(description="Human readable message"),
        "access_token": fields.String(description="JWT access token"),
        "user": fields.Raw(description="Authenticated user information")
    }
)

register_success_response_model = api.model(
    "RegisterSuccessResponse",
    {
        "status": fields.String(description="Operation status"),
        "message": fields.String(description="Human readable message"),
        "user": fields.Raw(description="Created user information")
    }
)

error_response_model = api.model(
    "ErrorResponse",
    {
        "status": fields.String(description="Operation status"),
        "message": fields.String(description="Error message")
    }
)