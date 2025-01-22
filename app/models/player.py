import uuid
from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Index, SQLModel


# Properties to receive on player creation
class PlayerCreate(SQLModel):
    user_public_id: uuid.UUID = Field()
    telegram_id: int | None = Field(default=None)


# Properties to receive on player update
class PlayerUpdate(SQLModel):
    MIN_TIME_AVAILABILITY: ClassVar[int] = 1
    MAX_TIME_AVAILABILITY: ClassVar[int] = 7

    time_availability: int | None = Field(
        default=None, ge=MIN_TIME_AVAILABILITY, le=MAX_TIME_AVAILABILITY
    )


# Shared properties
class PlayerBase(PlayerCreate, PlayerUpdate):
    zone_km: int | None = Field(default=None)
    zone_location: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)


# Database model, database table inferred from class name
class Player(PlayerBase, table=True):
    __tablename__ = "players"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (
        Index("id", "user_public_id"),
        UniqueConstraint("user_public_id", name="uq_player_constraint"),
    )


# Properties to return via API, id is always required
class PlayerPublic(PlayerBase):
    pass
