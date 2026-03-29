def success_response(message: str, data=None, extra: dict | None = None) -> dict:
    response = {
        "status": "success",
        "message": message
    }

    if data is not None:
        response["data"] = data

    if extra:
        response.update(extra)

    return response


def error_response(message: str) -> dict:
    return {
        "status": "failed",
        "message": message
    }