from __future__ import annotations

from enum import IntEnum
from typing import ClassVar
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Index, SQLModel


class WeekDay(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


# Shared properties
class PlayerAvailabilityBase(SQLModel):
    _BEGIN_DAY: ClassVar[int] = WeekDay.MONDAY
    _LAST_DAY: ClassVar[int] = WeekDay.SUNDAY

    week_day: WeekDay = Field(default=WeekDay.MONDAY)
    is_available: bool = Field(default=False)

    @classmethod
    def valid_days(cls) -> list[WeekDay]:
        return list(WeekDay)


# Shared private properties
class PlayerAvailabilityImmutable(SQLModel):
    user_public_id: UUID = Field()


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


class PlayerAvailabilityList(SQLModel):
    available_days: list[PlayerAvailabilityBase]

    def to_public(self, user_public_id: UUID) -> PlayerAvailabilityListPublic:
        return PlayerAvailabilityListPublic(
            user_public_id=user_public_id, available_days=self.available_days
        )


class PlayerAvailabilityListUpdate(PlayerAvailabilityList):
    pass


class PlayerAvailabilityListPublic(PlayerAvailabilityList, PlayerAvailabilityImmutable):
    pass
