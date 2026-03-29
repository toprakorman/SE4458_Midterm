from app.extensions import db


class Passenger(db.Model):
    __tablename__ = "passengers"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    seat_number = db.Column(db.String(10), nullable=True)
    checked_in = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "full_name": self.full_name,
            "seat_number": self.seat_number,
            "checked_in": self.checked_in
        }