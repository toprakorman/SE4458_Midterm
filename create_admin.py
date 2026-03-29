from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    email = "admin@airline.com"

    existing_admin = User.query.filter_by(email=email).first()
    if existing_admin:
        print("Admin already exists.")
    else:
        admin = User(
            username="admin",
            email=email,
            role="admin"
        )
        admin.set_password("Admin123!")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")