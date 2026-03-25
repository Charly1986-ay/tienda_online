import math

def create_pagination(page: int, limit: int, count: int):
    total_pages = max(1, math.ceil(count / limit))
    page = min(page, total_pages)  # evita page fuera de rango
    skip = (page - 1) * limit
    return (page, skip, total_pages)