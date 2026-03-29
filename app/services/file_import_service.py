from app.services.flight_service import FlightService
from app.utils.csv_parser import parse_flights_csv
from app.utils.response_helpers import success_response, error_response


class FileImportService:
    @staticmethod
    def import_flights_from_csv(file_storage):
        rows, parse_error = parse_flights_csv(file_storage)
        if parse_error:
            return error_response(parse_error), 400

        inserted_count = 0
        failed_count = 0
        errors = []

        for index, row in enumerate(rows, start=2):  # row 1 is header
            try:
                payload = {
                    "flight_number": row.get("flight_number", ""),
                    "date_from": row.get("date_from", ""),
                    "date_to": row.get("date_to", ""),
                    "airport_from": row.get("airport_from", ""),
                    "airport_to": row.get("airport_to", ""),
                    "duration": int(row.get("duration")) if row.get("duration") else None,
                    "capacity": int(row.get("capacity")) if row.get("capacity") else None,
                }

                _, status_code = FlightService.add_flight(payload)

                if status_code == 201:
                    inserted_count += 1
                else:
                    failed_count += 1
                    errors.append(
                        {
                            "row": index,
                            "message": "Invalid flight data or duplicate flight"
                        }
                    )

            except ValueError:
                failed_count += 1
                errors.append(
                    {
                        "row": index,
                        "message": "duration and capacity must be integers"
                    }
                )
            except Exception as exc:
                failed_count += 1
                errors.append(
                    {
                        "row": index,
                        "message": str(exc)
                    }
                )

        return success_response(
            "File processed successfully",
            data={
                "inserted_count": inserted_count,
                "failed_count": failed_count,
                "errors": errors
            }
        ), 200