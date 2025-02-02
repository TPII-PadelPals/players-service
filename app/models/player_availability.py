from uuid import UUID

from sqlmodel import Field, Index, SQLModel


# Shared properties
class PlayerAvailabilityBase(SQLModel):
    week_day: int | None = Field(default=None)
    is_available: bool | None = Field(default=None)


# Shared private properties
class PlayerAvailabilityImmutable(SQLModel):
    user_public_id: UUID = Field()


# Properties to receive on player creation
class PlayerAvailabilityCreate(SQLModel):
    available_days: list[int] = Field()
    pass


# Database model, database table inferred from class name
class PlayerAvailability(
    PlayerAvailabilityBase, PlayerAvailabilityImmutable, table=True
):
    __tablename__ = "players_availability"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (
        Index(f"idx{__tablename__}", "user_public_id"),
        # UniqueConstraint("user_public_id", name="uq_player_constraint"),
    )


# Properties to return via API, id is always required
class PlayerAvailabilityPublic(PlayerAvailabilityImmutable, PlayerAvailabilityCreate):
    pass
