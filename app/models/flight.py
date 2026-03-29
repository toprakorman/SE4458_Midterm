from datetime import datetime

from app.extensions import db


class Flight(db.Model):
    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(20), nullable=False)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    airport_from = db.Column(db.String(10), nullable=False)
    airport_to = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    bookings = db.relationship("Booking", backref="flight", lazy=True)

    __table_args__ = (
        db.UniqueConstraint(
            "flight_number",
            "date_from",
            name="uq_flight_number_date_from"
        ),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "date_from": self.date_from.isoformat(),
            "date_to": self.date_to.isoformat(),
            "airport_from": self.airport_from,
            "airport_to": self.airport_to,
            "duration": self.duration,
            "capacity": self.capacity,
            "available_seats": self.available_seats,
            "created_at": self.created_at.isoformat()
        }