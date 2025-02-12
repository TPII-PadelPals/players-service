from typing import ClassVar
from uuid import UUID

from sqlalchemy import UniqueConstraint
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
