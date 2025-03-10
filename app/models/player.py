from typing import Any, ClassVar
from uuid import UUID

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.sql.expression import and_
from sqlmodel import Field, Index, SQLModel


# Shared properties
class PlayerBase(SQLModel):
    MIN_TIME_AVAILABILITY: ClassVar[int] = 1
    MAX_TIME_AVAILABILITY: ClassVar[int] = 7

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
    def _coords_conditions(self, data: dict[str, Any]) -> list[Any]:
        latitude = data.pop("latitude", None)
        longitude = data.pop("longitude", None)
        if latitude is None or longitude is None:
            return []
        coords_conditions = [
            Player.latitude.isnot(None),  # type: ignore
            Player.longitude.isnot(None),  # type: ignore
            Player.search_range_km.isnot(None),  # type: ignore
            func.sqrt(
                func.pow(Player.latitude - latitude, 2)  # type: ignore
                + func.pow(Player.longitude - longitude, 2)  # type: ignore
            )
            < Player.search_range_km,
        ]
        return coords_conditions

    def _equal_conditions(self, data: dict[str, Any]) -> list[Any]:
        equal_conditions = []
        for attr, value in data.items():
            if value is not None:
                equal_conditions.append(getattr(Player, attr) == value)
        return equal_conditions

    def to_sqlalchemy(self) -> Any:
        data = self.model_dump(exclude_unset=True)
        coords_conditions = self._coords_conditions(data)
        equal_conditions = self._equal_conditions(data)
        all_conditions = coords_conditions + equal_conditions
        return and_(*all_conditions)


class PlayerListPublic(SQLModel):
    data: list[PlayerPublic]


class PlayerList(SQLModel):
    data: list[Player]

    def to_public(self) -> PlayerListPublic:
        return PlayerListPublic.model_validate(self)
