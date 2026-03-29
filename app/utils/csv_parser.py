import csv
import io


REQUIRED_FLIGHT_COLUMNS = {
    "flight_number",
    "date_from",
    "date_to",
    "airport_from",
    "airport_to",
    "duration",
    "capacity"
}


def parse_flights_csv(file_storage):
    """
    Accepts a Werkzeug FileStorage object and returns:
    - rows: list[dict]
    - error: str | None
    """
    if not file_storage:
        return None, "CSV file is required"

    filename = (file_storage.filename or "").lower()
    if not filename.endswith(".csv"):
        return None, "Only .csv files are allowed"

    try:
        content = file_storage.read().decode("utf-8-sig")
        stream = io.StringIO(content)
        reader = csv.DictReader(stream)

        if not reader.fieldnames:
            return None, "CSV file is empty or invalid"

        normalized_headers = {header.strip() for header in reader.fieldnames if header}
        missing = REQUIRED_FLIGHT_COLUMNS - normalized_headers
        if missing:
            return None, f"Missing required CSV columns: {', '.join(sorted(missing))}"

        rows = []
        for row in reader:
            normalized_row = {
                (key.strip() if key else key): (value.strip() if value else value)
                for key, value in row.items()
            }
            rows.append(normalized_row)

        return rows, None

    except UnicodeDecodeError:
        return None, "CSV file must be UTF-8 encoded"
    except Exception as exc:
        return None, f"Failed to parse CSV file: {str(exc)}"