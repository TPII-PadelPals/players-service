from typing import Any

from sqlalchemy import Function, func


def distance_radians_sql(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> Function[Any]:
    return func.acos(
        func.sin(func.radians(x1)) * func.sin(func.radians(x2))
        + func.cos(func.radians(x1))
        * func.cos(func.radians(x2))
        * func.cos(func.radians(y2) - (func.radians(y1)))
    )
