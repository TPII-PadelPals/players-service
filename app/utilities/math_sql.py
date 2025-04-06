from typing import Any

from sqlalchemy import ColumnElement, func

EARTH_RADIUS_KM: float = 6378.0


def distance_haversine_sql(
    x_lat: float, y_lat: float, x_lon: float, y_lon: float
) -> ColumnElement[Any]:
    return 2 * func.asin(
        func.sqrt(
            func.pow(func.sin((func.radians(x_lat) - func.radians(y_lat)) / 2), 2)
            + func.cos(func.radians(x_lat))
            * func.cos(func.radians(y_lat))
            * func.pow(func.sin((func.radians(x_lon) - func.radians(y_lon)) / 2), 2)
        )
    )


def km_to_rads(km: float) -> float:
    return km / EARTH_RADIUS_KM
