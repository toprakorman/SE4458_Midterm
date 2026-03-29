from flask import Flask
from flask_restx import Api

from app.config import Config
from app.extensions import db, jwt, limiter
from app.models import register_models


api = Api(
    title="Airline Ticketing API",
    version="1.0",
    description="Midterm project for airline ticketing system",
    doc="/swagger",
    authorizations={
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Type: Bearer <your_jwt_token>"
        }
    },
    security="Bearer"
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    initialize_extensions(app)
    register_models()
    register_namespaces()

    return app


def initialize_extensions(app: Flask) -> None:
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    api.init_app(app)


def register_namespaces() -> None:
    from app.routes.auth_routes import auth_ns
    from app.routes.flight_routes import flight_ns
    from app.routes.booking_routes import booking_ns
    from app.routes.checkin_routes import checkin_ns
    from app.routes.passenger_routes import passenger_ns

    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(flight_ns, path="/api/v1/flights")
    api.add_namespace(booking_ns, path="/api/v1/bookings")
    api.add_namespace(checkin_ns, path="/api/v1/checkin")
    api.add_namespace(passenger_ns, path="/api/v1/passengers")