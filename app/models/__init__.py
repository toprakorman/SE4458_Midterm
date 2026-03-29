from app.models.user import User
from app.models.flight import Flight
from app.models.booking import Booking
from app.models.passenger import Passenger


def register_models() -> None:
    """
    Import models so SQLAlchemy recognizes them before migrations/database creation.
    """
    _ = User
    _ = Flight
    _ = Booking
    _ = Passenger