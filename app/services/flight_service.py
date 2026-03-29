from app.extensions import db
from app.models.flight import Flight
from app.utils.pagination import build_pagination_response
from app.utils.response_helpers import success_response, error_response
from app.utils.validators import parse_iso_datetime, parse_date_only, is_positive_integer


class FlightService:
    @staticmethod
    def add_flight(data: dict):
        flight_number = data.get("flight_number", "").strip().upper()
        date_from_raw = data.get("date_from", "").strip()
        date_to_raw = data.get("date_to", "").strip()
        airport_from = data.get("airport_from", "").strip().upper()
        airport_to = data.get("airport_to", "").strip().upper()
        duration = data.get("duration")
        capacity = data.get("capacity")

        if not all([flight_number, date_from_raw, date_to_raw, airport_from, airport_to]):
            return error_response("All flight fields are required"), 400

        if not is_positive_integer(duration):
            return error_response("duration must be a positive integer"), 400

        if not is_positive_integer(capacity):
            return error_response("capacity must be a positive integer"), 400

        date_from = parse_iso_datetime(date_from_raw)
        date_to = parse_iso_datetime(date_to_raw)

        if not date_from or not date_to:
            return error_response("date_from and date_to must be valid ISO datetime strings"), 400

        if date_to <= date_from:
            return error_response("date_to must be later than date_from"), 400

        if airport_from == airport_to:
            return error_response("airport_from and airport_to cannot be the same"), 400

        existing_flight = Flight.query.filter_by(
            flight_number=flight_number,
            date_from=date_from
        ).first()

        if existing_flight:
            return error_response("Flight already exists for this flight_number and date_from"), 409

        new_flight = Flight(
            flight_number=flight_number,
            date_from=date_from,
            date_to=date_to,
            airport_from=airport_from,
            airport_to=airport_to,
            duration=duration,
            capacity=capacity,
            available_seats=capacity
        )

        db.session.add(new_flight)
        db.session.commit()

        return success_response(
            "Flight added successfully",
            data=new_flight.to_dict()
        ), 201

    @staticmethod
    def search_flights(args, page: int, per_page: int):
        date_from_raw = (args.get("date_from") or "").strip()
        airport_from = (args.get("airport_from") or "").strip().upper()
        airport_to = (args.get("airport_to") or "").strip().upper()
        people_raw = (args.get("people") or "1").strip()
        trip_type = (args.get("trip_type") or "one_way").strip().lower()

        if not date_from_raw or not airport_from or not airport_to:
            return error_response(
                "date_from, airport_from, and airport_to are required query parameters"
            ), 400

        search_date = parse_date_only(date_from_raw)
        if not search_date:
            return error_response("date_from must be in YYYY-MM-DD format"), 400

        try:
            people = int(people_raw)
        except ValueError:
            return error_response("people must be a valid integer"), 400

        if people < 1:
            return error_response("people must be at least 1"), 400

        if trip_type not in {"one_way", "round_trip"}:
            return error_response("trip_type must be one_way or round_trip"), 400

        query = Flight.query.filter(
            db.func.date(Flight.date_from) == search_date,
            Flight.airport_from == airport_from,
            Flight.airport_to == airport_to,
            Flight.available_seats >= people
        ).order_by(Flight.date_from.asc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        items = []
        for flight in pagination.items:
            items.append(
                {
                    "flight_number": flight.flight_number,
                    "date_from": flight.date_from.isoformat(),
                    "date_to": flight.date_to.isoformat(),
                    "airport_from": flight.airport_from,
                    "airport_to": flight.airport_to,
                    "duration": flight.duration,
                    "available_seats": flight.available_seats
                }
            )

        paginated_data = build_pagination_response(pagination, items)

        response = success_response("Flights fetched successfully")
        response.update(paginated_data)

        return response, 200