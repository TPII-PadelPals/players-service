from typing import Any, ClassVar
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.sql.expression import and_
from sqlmodel import Field, Index, SQLModel

from app.models.player_availability import PlayerAvailability, WeekDay
from app.utilities.math_sql import distance_haversine_sql, km_to_rads


# Shared properties
class PlayerBase(SQLModel):
    MIN_TIME_AVAILABILITY: ClassVar[int] = 1
    MAX_TIME_AVAILABILITY: ClassVar[int] = 7
    TIME_AVAILABILITY_SETS: ClassVar[dict[int, set[int]]] = {
        1: {1, 4, 5, 7},
        2: {2, 4, 6, 7},
        3: {3, 5, 6, 7},
        4: {1, 2, 4, 5, 6, 7},
        5: {1, 3, 4, 5, 6, 7},
        6: {2, 3, 4, 5, 6, 7},
        7: {1, 2, 3, 4, 5, 6, 7},
    }

    search_range_km: int | None = Field(default=None)
    address: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    time_availability: int | None = Field(
        default=None, ge=MIN_TIME_AVAILABILITY, le=MAX_TIME_AVAILABILITY
    )


# Shared private properties
class PlayerImmutable(SQLModel):
    user_public_id: UUID = Field()
    telegram_id: int | None = Field(default=None)


# Properties to receive on player creation
class PlayerCreate(PlayerImmutable):
    pass


# Properties to receive on player update
class PlayerUpdate(PlayerBase):
    pass


# Properties to return via API, id is always required
class PlayerPublic(PlayerBase, PlayerImmutable):
    pass


# Database model, database table inferred from class name
class Player(PlayerBase, PlayerImmutable, table=True):
    __tablename__ = "players"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (
        Index("id", "user_public_id"),
        UniqueConstraint("user_public_id", name="uq_player_constraint"),
    )


class PlayerFilters(PlayerBase):
    available_days: list[WeekDay] | None = Field(default=None)
    user_public_id: UUID | None = Field(default=None)
    n_players: int | None = Field(default=None)

    def _get_available_days_conditions(self, data: dict[str, Any]) -> list[Any]:
        avail_days = data.pop("available_days", None)
        if avail_days is None or len(avail_days) == 0:
            return []
        avail_days_conditions = [
            Player.user_public_id == PlayerAvailability.user_public_id
        ]
        for avail_day in avail_days:
            avail_days_conditions.append(PlayerAvailability.week_day == avail_day)
        return avail_days_conditions

    def _get_time_conditions(self, data: dict[str, Any]) -> list[Any]:
        time = data.pop("time_availability", None)
        if time is None:
            return []
        time_conditions = [
            Player.time_availability.isnot(None),  # type: ignore
            Player.time_availability.in_(  # type: ignore
                self.TIME_AVAILABILITY_SETS[time]
            ),
        ]
        return time_conditions

    def _get_coords_conditions(self, data: dict[str, Any]) -> list[Any]:
        latitude = data.pop("latitude", None)
        longitude = data.pop("longitude", None)
        if latitude is None or longitude is None:
            return []
        coords_conditions = [
            Player.latitude.isnot(None),  # type: ignore
            Player.longitude.isnot(None),  # type: ignore
            Player.search_range_km.isnot(None),  # type: ignore
            distance_haversine_sql(
                Player.latitude,  # type: ignore
                latitude,
                Player.longitude,  # type: ignore
                longitude,
            )
            < km_to_rads(
                Player.search_range_km  # type: ignore
            ),
        ]
        return coords_conditions

    def _get_equal_conditions(self, data: dict[str, Any]) -> list[Any]:
        equal_conditions = []
        for attr, value in data.items():
            equal_conditions.append(getattr(Player, attr) == value)
        return equal_conditions

    def to_sqlalchemy(self) -> Any:
        data = self.model_dump(exclude_unset=True, exclude_none=True)
        all_conditions = []
        all_conditions += self._get_available_days_conditions(data)
        all_conditions += self._get_time_conditions(data)
        all_conditions += self._get_coords_conditions(data)
        all_conditions += self._get_equal_conditions(data)
        return and_(True, *all_conditions)


class PlayerListPublic(SQLModel):
    data: list[PlayerPublic]


class PlayerList(SQLModel):
    data: list[Player]

    def to_public(self) -> PlayerListPublic:
        return PlayerListPublic.model_validate(self)
