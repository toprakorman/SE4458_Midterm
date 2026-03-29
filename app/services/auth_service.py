from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User


class AuthService:
    @staticmethod
    def register_user(data: dict) -> tuple[dict, int]:
        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()
        role = data.get("role", "customer").strip().lower()

        if not username or not email or not password:
            return {
                "status": "failed",
                "message": "username, email, and password are required"
            }, 400

        if role not in {"admin", "customer"}:
            return {
                "status": "failed",
                "message": "role must be either admin or customer"
            }, 400

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            return {
                "status": "failed",
                "message": "Username already exists"
            }, 409

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return {
                "status": "failed",
                "message": "Email already exists"
            }, 409

        new_user = User(
            username=username,
            email=email,
            role=role
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {
            "status": "success",
            "message": "User registered successfully",
            "user": new_user.to_dict()
        }, 201

    @staticmethod
    def login_user(data: dict) -> tuple[dict, int]:
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return {
                "status": "failed",
                "message": "email and password are required"
            }, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {
                "status": "failed",
                "message": "Invalid email or password"
            }, 401

        if not user.check_password(password):
            return {
                "status": "failed",
                "message": "Invalid email or password"
            }, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.role,
                "username": user.username
            }
        )

        return {
            "status": "success",
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }, 200