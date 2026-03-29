import random
from datetime import datetime

from app.extensions import db
from app.models.flight import Flight
from app.models.booking import Booking
from app.models.passenger import Passenger
from app.utils.response_helpers import success_response, error_response
from app.utils.validators import parse_date_only


class BookingService:

    @staticmethod
    def generate_ticket_number() -> str:
        now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        rand = random.randint(1000, 9999)
        return f"TKT-{now}-{rand}"

    @staticmethod
    def buy_ticket(data: dict, user_id: int):

        flight_number = data.get("flight_number", "").strip().upper()
        date_raw = data.get("date", "").strip()
        passenger_names = data.get("passenger_names", [])
        trip_type = data.get("trip_type", "one_way")

        # Validation
        if not flight_number or not date_raw or not passenger_names:
            return error_response("flight_number, date and passenger_names are required"), 400

        if not isinstance(passenger_names, list) or len(passenger_names) == 0:
            return error_response("passenger_names must be a non-empty list"), 400

        flight_date = parse_date_only(date_raw)
        if not flight_date:
            return error_response("date must be YYYY-MM-DD"), 400

        # Find flight
        flight = Flight.query.filter(
            db.func.date(Flight.date_from) == flight_date,
            Flight.flight_number == flight_number
        ).first()

        if not flight:
            return error_response("Flight not found"), 404

        passenger_count = len(passenger_names)

        # Check capacity
        if flight.available_seats < passenger_count:
            return error_response("Sold out"), 400

        # Create booking
        ticket_number = BookingService.generate_ticket_number()

        booking = Booking(
            ticket_number=ticket_number,
            flight_id=flight.id,
            user_id=user_id,
            passenger_count=passenger_count,
            trip_type=trip_type
        )

        db.session.add(booking)
        db.session.flush()  # important to get booking.id

        # Create passengers
        for name in passenger_names:
            passenger = Passenger(
                booking_id=booking.id,
                full_name=name.strip()
            )
            db.session.add(passenger)

        # Reduce seats
        flight.available_seats -= passenger_count

        db.session.commit()

        return success_response(
            "Ticket purchased successfully",
            data={
                "ticket_number": ticket_number
            }
        ), 201