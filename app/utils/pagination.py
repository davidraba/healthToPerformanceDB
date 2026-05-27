from app.config import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT


def normalize_pagination(limit: int | None, offset: int | None) -> tuple[int, int]:
    if limit is None or limit < 1:
        limit = DEFAULT_PAGE_LIMIT
    if limit > MAX_PAGE_LIMIT:
        limit = MAX_PAGE_LIMIT
    if offset is None or offset < 0:
        offset = 0
    return limit, offset
