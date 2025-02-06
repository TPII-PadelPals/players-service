import uuid
from typing import ClassVar
from sqlmodel import Field, SQLModel, Index, SQLModel, UniqueConstraint


# BASE_BEGINNER = 1.0
# BASE_INTERMEDIATE = 2.0
# BASE_ADVANCE = 3.0
# CATEGORIZATION = [BASE_INTERMEDIATE, BASE_ADVANCE]
# DEFINITION_OF_CATEGORIZATION = ["Beginner", "Intermediate", "Advanced"]
# BASE_SKILL_NEW = BASE_BEGINNER


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
    CATEGORIZATION: ClassVar[float] = [BASE_INTERMEDIATE, BASE_ADVANCE]

    serve: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    forehand_ground: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    background_ground: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    forehand_back_wall: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    backhand_back_wall: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    forehand_side_wall: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    backhand_side_wall: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    forehand_double_walls: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    backhand_double_walls: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    forehand_counter_wall: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    backhand_counter_wall: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    forehand_volley: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    backhand_volley: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    lob: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    smash: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)
    bandeja: float | None = Field(default=BASE_SKILL_NEW, ge=LIMIT_MIN_OF_SKILL, le=LIMIT_MAX_OF_SKILL)


# Shared private properties
class StrokeImmutable(SQLModel):
    user_public_id: uuid.UUID = Field()


# Properties to receive on item creation
class StrokeCreate(StrokeBase):
    def create_stroke_skill(self, user_public_id: uuid.UUID):
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
            bandeja=self.BASE_SKILL_NEW
        )
        result.update_from_stroke_create(self)
        return result


# Properties to receive on item update
class StrokeUpdate(StrokeBase):
    pass


# Database model, database table inferred from class name
class Stroke(StrokeBase, StrokeImmutable, table=True):
    __tablename__ = "strokes"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (
        # Index("id", "user_public_id"),
        UniqueConstraint("user_public_id", name="uq_stroke_constraint"),
    )


    # @classmethod
    # def auto_test_for_skill(cls, autovalue_skill: str):
    #     # cuando el usuario se auto-evalua escribe con palabras, retorna el valor a ser almaceenado
    #     match autovalue_skill.lower():
    #         case "beginner":
    #             return cls.BASE_BEGINNER
    #         case "intermediate":
    #             return cls.BASE_INTERMEDIATE
    #         case "advanced":
    #             return cls.BASE_ADVANCE
    #         case _:
    #             # ver si no conviene hacer un raise exception
    #             return None
    #
    #
    # def update_from_stroke_create(self, info: StrokeCreate):
    #     for field in self.__dict__:
    #         if field[0] == "_":
    #             continue
    #         value = getattr(info, field, None)
    #         if value is not None:
    #             setattr(self, field, self.auto_test_for_skill(value))

    def update_from_stroke_create(self, info: StrokeCreate):
        for field in self.__dict__:
            if field[0] == "_":
                continue
            value = getattr(info, field, None)
            if value is not None:
                setattr(self, field, value)


    # @classmethod
    # def skill_categorization(cls, value_from_skill: float):
    #     return cls.DEFINITION_OF_CATEGORIZATION[cls.skill_categorization_value(value_from_skill)]


    @classmethod
    def skill_categorization_value(cls, value_from_skill: float):
        size_categorization = len(cls.CATEGORIZATION)
        for i in range(size_categorization):
            if value_from_skill < cls.CATEGORIZATION[i]:
                return i
        return size_categorization

    def generate_stroke_public(self):
        public = StrokePublic(user_public_id=self.user_public_id)
        for field in self.__dict__:
            if field == "user_public_id" or field[0] == "_":
                continue
            value = getattr(self, field)
            setattr(public, field, self.skill_categorization(value))
        return public


# Properties to return via API, id is always required
class StrokePublic(StrokeBase, StrokeImmutable):
    pass
