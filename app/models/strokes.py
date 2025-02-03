import uuid
from sqlmodel import Field, SQLModel, Index, SQLModel, UniqueConstraint


BASE_BEGINNER = 1.0
BASE_INTERMEDIATE = 2.0
BASE_ADVANCE = 3.0
CATEGORIZATION = [BASE_INTERMEDIATE, BASE_ADVANCE]
DEFINITION_OF_CATEGORIZATION = ["Beginner", "Intermediate", "Advanced"]
BASE_SKILL_NEW = BASE_BEGINNER


# Shared properties
class StrokeBase(SQLModel):
    BASE_BEGINNER = 1.0
    BASE_INTERMEDIATE = 2.0
    BASE_ADVANCE = 3.0
    LIMIT_MIN_OF_SKILL = BASE_BEGINNER
    LIMIT_MAX_OF_SKILL = BASE_ADVANCE + 1.0
    BASE_SKILL_NEW = BASE_BEGINNER

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



# Properties to receive on item creation
class StrokeCreate(StrokeBase):
    def create_stroke_skill(self, user_public_id: uuid.UUID):
        result = Stroke(
            user_public_id=user_public_id,
            serve=BASE_SKILL_NEW,
            forehand_ground=BASE_SKILL_NEW,
            background_ground=BASE_SKILL_NEW,
            forehand_back_wall=BASE_SKILL_NEW,
            backhand_back_wall=BASE_SKILL_NEW,
            forehand_side_wall=BASE_SKILL_NEW,
            backhand_side_wall=BASE_SKILL_NEW,
            forehand_double_walls=BASE_SKILL_NEW,
            backhand_double_walls=BASE_SKILL_NEW,
            forehand_counter_wall=BASE_SKILL_NEW,
            backhand_counter_wall=BASE_SKILL_NEW,
            forehand_volley=BASE_SKILL_NEW,
            backhand_volley=BASE_SKILL_NEW,
            lob=BASE_SKILL_NEW,
            smash=BASE_SKILL_NEW,
            bandeja=BASE_SKILL_NEW
        )
        result.update_from_stroke_create(self)
        return result


# Properties to receive on item update
class StrokeUpdate(StrokeBase):
    pass


# Database model, database table inferred from class name
class Stroke(StrokeBase, table=True):
    user_public_id: uuid.UUID = Field()
    id: int = Field(primary_key=True)
    __tablename__ = "strokes"
    __table_args__ = (
        Index("id", "user_public_id"),
        UniqueConstraint("user_public_id", name="uq_player_constraint"),
    )


    @classmethod
    def auto_test_for_skill(cls, autovalue_skill: str):
        # cuando el usuario se auto-evalua escribe con palabras, retorna el valor a ser almaceenado
        match autovalue_skill.lower():
            case "beginner":
                return BASE_BEGINNER
            case "intermediate":
                return BASE_INTERMEDIATE
            case "advanced":
                return BASE_ADVANCE
            case _:
                # ver si no conviene hacer un raise exception
                return None


    def update_from_stroke_create(self, info: StrokeCreate):
        for field in self.__dict__:
            if field[0] == "_":
                continue
            value = getattr(info, field, None)
            if value is not None:
                setattr(self, field, self.auto_test_for_skill(value))


    @classmethod
    def skill_categorization(cls, value_from_skill: float):
        return DEFINITION_OF_CATEGORIZATION[cls.skill_categorization_value(value_from_skill)]


    @classmethod
    def skill_categorization_value(cls, value_from_skill: float):
        size_categorization = len(CATEGORIZATION)
        for i in range(size_categorization):
            if value_from_skill < CATEGORIZATION[i]:
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
class StrokePublic(StrokeBase):
    user_public_id: uuid.UUID = Field(primary_key=True)

