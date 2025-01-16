import uuid

from sqlmodel import Field, Index, SQLModel


# Shared properties
class PlayerBase(SQLModel):
    user_public_id: uuid.UUID = Field(unique=True)
    telegram_id: int | None = Field(default=None)
    zone_km: int | None = Field(default=None)
    zone_location: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    time_availability: int | None = Field(default=None)


# Properties to receive on player creation
class PlayerCreate(PlayerBase):
    pass


# Database model, database table inferred from class name
class Player(PlayerBase, table=True):
    __tablename__ = "players"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (Index("id", "user_public_id"),)


# Properties to return via API, id is always required
class PlayerPublic(PlayerBase):
    pass
