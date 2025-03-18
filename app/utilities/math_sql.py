from typing import Any

from sqlalchemy import Function, func


def distance_euclidean_sql(x1: float, y1: float, x2: float, y2: float) -> Function[Any]:
    return func.sqrt(func.pow(x1 - x2, 2) + func.pow(y1 - y2, 2))
