def get_pagination_params(args) -> tuple[int, int]:
    try:
        page = int(args.get("page", 1))
    except (TypeError, ValueError):
        page = 1

    try:
        per_page = int(args.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10

    if page < 1:
        page = 1

    if per_page < 1:
        per_page = 10

    if per_page > 10:
        per_page = 10

    return page, per_page


def build_pagination_response(pagination_obj, items: list) -> dict:
    return {
        "page": pagination_obj.page,
        "per_page": pagination_obj.per_page,
        "total": pagination_obj.total,
        "pages": pagination_obj.pages,
        "data": items
    }