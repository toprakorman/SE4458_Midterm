from app.extensions import db
from app.models.flight import Flight
from app.models.passenger import Passenger
from app.utils.response_helpers import success_response, error_response
from app.utils.validators import parse_date_only


class CheckInService:

    @staticmethod
    def generate_seat_number(flight_id: int) -> str:
        """
        Simple seat assignment:
        count existing checked-in passengers and assign next number
        """
        count = Passenger.query.join(
            Passenger.booking
        ).filter(
            Passenger.checked_in == True,
            Passenger.booking.has(flight_id=flight_id)
        ).count()

        return str(count + 1)

    @staticmethod
    def check_in(data: dict):

        flight_number = data.get("flight_number", "").strip().upper()
        date_raw = data.get("date", "").strip()
        passenger_name = data.get("passenger_name", "").strip()

        if not flight_number or not date_raw or not passenger_name:
            return error_response("All fields are required"), 400

        flight_date = parse_date_only(date_raw)
        if not flight_date:
            return error_response("Invalid date format"), 400

        # Find flight
        flight = Flight.query.filter(
            db.func.date(Flight.date_from) == flight_date,
            Flight.flight_number == flight_number
        ).first()

        if not flight:
            return error_response("Flight not found"), 404

        # Find passenger
        passenger = Passenger.query.join(
            Passenger.booking
        ).filter(
            Passenger.full_name == passenger_name,
            Passenger.booking.has(flight_id=flight.id)
        ).first()

        if not passenger:
            return error_response("Passenger not found"), 404

        if passenger.checked_in:
            return error_response("Passenger already checked in"), 400

        # Assign seat
        seat_number = CheckInService.generate_seat_number(flight.id)

        passenger.checked_in = True
        passenger.seat_number = seat_number

        db.session.commit()

        return success_response(
            "Check-in successful",
            data={"seat_number": seat_number}
        ), 200