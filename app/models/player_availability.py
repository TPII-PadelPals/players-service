from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Index, SQLModel


# Shared properties
class PlayerAvailabilityBase(SQLModel):
    week_day: int = Field(default=None)
    is_available: bool = Field(default=False)


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
        UniqueConstraint(
            "user_public_id", "week_day", name="uq_player_availability_constraint"
        ),
    )

    def set_available(self):
        self.week_day = True


# Properties to return via API, id is always required
class PlayerAvailabilityPublic(PlayerAvailabilityImmutable, PlayerAvailabilityCreate):
    pass
