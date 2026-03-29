from app.extensions import db
from app.models.flight import Flight
from app.models.passenger import Passenger
from app.utils.pagination import build_pagination_response
from app.utils.response_helpers import success_response, error_response
from app.utils.validators import parse_date_only


class PassengerService:

    @staticmethod
    def get_passenger_list(args, page: int, per_page: int):

        flight_number = (args.get("flight_number") or "").strip().upper()
        date_raw = (args.get("date") or "").strip()

        if not flight_number or not date_raw:
            return error_response("flight_number and date are required"), 400

        flight_date = parse_date_only(date_raw)
        if not flight_date:
            return error_response("Invalid date format"), 400

        flight = Flight.query.filter(
            db.func.date(Flight.date_from) == flight_date,
            Flight.flight_number == flight_number
        ).first()

        if not flight:
            return error_response("Flight not found"), 404

        query = Passenger.query.join(
            Passenger.booking
        ).filter(
            Passenger.booking.has(flight_id=flight.id)
        )

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        items = []
        for p in pagination.items:
            items.append({
                "passenger_name": p.full_name,
                "seat_number": p.seat_number,
                "checked_in": p.checked_in
            })

        paginated_data = build_pagination_response(pagination, items)

        response = success_response("Passenger list fetched successfully")
        response.update(paginated_data)

        return response, 200