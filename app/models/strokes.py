from __future__ import annotations

import uuid
from typing import ClassVar

from sqlmodel import Field, SQLModel, UniqueConstraint


# Shared properties
class StrokeBase(SQLModel):
    # must always be fulfilled
    # LIMIT_MIN_OF_SKILL <= BASE_BEGINNER < BASE_INTERMEDIATE < BASE_ADVANCE <= LIMIT_MAX_OF_SKILL
    BASE_BEGINNER: ClassVar[float] = 1.0
    BASE_INTERMEDIATE: ClassVar[float] = 2.0
    BASE_ADVANCE: ClassVar[float] = 3.0
    LIMIT_MIN_OF_SKILL: ClassVar[float] = BASE_BEGINNER
    LIMIT_MAX_OF_SKILL: ClassVar[float] = BASE_ADVANCE + 1.0
    BASE_SKILL_NEW: ClassVar[float] = BASE_BEGINNER
    CATEGORIZATION: ClassVar[list[float]] = [BASE_INTERMEDIATE, BASE_ADVANCE]

    serve: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    forehand_ground: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    background_ground: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    forehand_back_wall: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    backhand_back_wall: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    forehand_side_wall: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    backhand_side_wall: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    forehand_double_walls: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    backhand_double_walls: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    forehand_counter_wall: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    backhand_counter_wall: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    forehand_volley: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    backhand_volley: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    lob: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    smash: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )
    bandeja: float | None = Field(
        default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL
    )


# Shared private properties
class StrokeImmutable(SQLModel):
    user_public_id: uuid.UUID = Field(foreign_key="players.user_public_id")


# Properties to receive on item creation
class StrokeCreate(StrokeBase):
    def from_public(self, user_public_id: uuid.UUID) -> Stroke:
        result = Stroke(
            user_public_id=user_public_id,
            serve=self.BASE_SKILL_NEW,
            forehand_ground=self.BASE_SKILL_NEW,
            background_ground=self.BASE_SKILL_NEW,
            forehand_back_wall=self.BASE_SKILL_NEW,
            backhand_back_wall=self.BASE_SKILL_NEW,
            forehand_side_wall=self.BASE_SKILL_NEW,
            backhand_side_wall=self.BASE_SKILL_NEW,
            forehand_double_walls=self.BASE_SKILL_NEW,
            backhand_double_walls=self.BASE_SKILL_NEW,
            forehand_counter_wall=self.BASE_SKILL_NEW,
            backhand_counter_wall=self.BASE_SKILL_NEW,
            forehand_volley=self.BASE_SKILL_NEW,
            backhand_volley=self.BASE_SKILL_NEW,
            lob=self.BASE_SKILL_NEW,
            smash=self.BASE_SKILL_NEW,
            bandeja=self.BASE_SKILL_NEW,
        )
        update_dict = self.model_dump(exclude_unset=True)
        result.sqlmodel_update(update_dict)
        return result


# Properties to receive on item update
class StrokeUpdate(StrokeBase):
    pass


# Database model, database table inferred from class name
class Stroke(StrokeBase, StrokeImmutable, table=True):
    __tablename__ = "strokes"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (UniqueConstraint("user_public_id", name="uq_stroke_constraint"),)


    @classmethod
    def skill_categorization_value(cls, value_from_skill: float) -> int:
        size_categorization = int(len(cls.CATEGORIZATION))
        for i in range(size_categorization):
            if value_from_skill < cls.CATEGORIZATION[i]:
                return i
        return size_categorization

    def to_public(self) -> StrokePublic:
        data = self.model_dump()
        public = StrokePublic(**data)
        return public


# Properties to return via API, id is always required
class StrokePublic(StrokeBase, StrokeImmutable):
    pass
