import uuid

from sqlmodel import Field, Index, SQLModel

MAX_TIME_AVAILABILITY = 7
MIN_TIME_AVAILABILITY = 1


# Properties to receive on player creation
class PlayerCreate(SQLModel):
    user_public_id: uuid.UUID = Field(unique=True)
    telegram_id: int | None = Field(default=None)


# Shared properties
class PlayerBase(PlayerCreate):
    zone_km: int | None = Field(default=None)
    zone_location: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    time_availability: int | None = Field(
        default=None, ge=MIN_TIME_AVAILABILITY, le=MAX_TIME_AVAILABILITY
    )


# Properties to receive on item update
class PlayerUpdate(SQLModel):
    time_availability: int | None = Field(
        default=None, ge=MIN_TIME_AVAILABILITY, le=MAX_TIME_AVAILABILITY
    )


# Database model, database table inferred from class name
class Player(PlayerBase, table=True):
    __tablename__ = "players"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (Index("id", "user_public_id"),)


# Properties to return via API, id is always required
class PlayerPublic(PlayerBase):
    pass
