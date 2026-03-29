from datetime import datetime

from app.extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    passenger_count = db.Column(db.Integer, nullable=False)
    trip_type = db.Column(db.String(20), nullable=False, default="one_way")
    booking_status = db.Column(db.String(20), nullable=False, default="confirmed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    passengers = db.relationship(
        "Passenger",
        backref="booking",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "flight_id": self.flight_id,
            "user_id": self.user_id,
            "passenger_count": self.passenger_count,
            "trip_type": self.trip_type,
            "booking_status": self.booking_status,
            "created_at": self.created_at.isoformat()
        }