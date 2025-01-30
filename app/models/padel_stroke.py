import uuid
from sqlmodel import Field, SQLModel


BASE_BEGINNER = 1.0
BASE_INTERMEDIATE = 2.0
BASE_ADVANCE = 3.0
CATEGORIZATION = [BASE_INTERMEDIATE, BASE_ADVANCE]
DEFINITION_OF_CATEGORIZATION = ["Beginner", "Intermediate", "Advanced"]
BASE_SKILL_NEW = BASE_BEGINNER


# Properties to receive on item creation
class PadelStrokeCreate(SQLModel):
    serve: str | None = Field(default=None)
    forehand_ground: str | None = Field(default=None)
    background_ground: str | None = Field(default=None)
    forehand_back_wall: str | None = Field(default=None)
    backhand_back_wall: str | None = Field(default=None)
    forehand_side_wall: str | None = Field(default=None)
    backhand_side_wall: str | None = Field(default=None)
    forehand_double_walls: str | None = Field(default=None)
    backhand_double_walls: str | None = Field(default=None)
    forehand_counter_wall: str | None = Field(default=None)
    backhand_counter_wall: str | None = Field(default=None)
    forehand_volley: str | None = Field(default=None)
    backhand_volley: str | None = Field(default=None)
    lob: str | None = Field(default=None)
    smash: str | None = Field(default=None)
    bandeja: str | None = Field(default=None)


    def create_padel_stroke_skill(self, user_public_id: uuid.UUID):
        result = PadelStroke(
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
        result.update_from_paddle_stroke_create(self)
        return result


# Shared properties
class PadelStrokeBase(SQLModel):
    serve: float = Field(default=BASE_SKILL_NEW)
    forehand_ground: float = Field(default=BASE_SKILL_NEW)
    background_ground: float = Field(default=BASE_SKILL_NEW)
    forehand_back_wall: float = Field(default=BASE_SKILL_NEW)
    backhand_back_wall: float = Field(default=BASE_SKILL_NEW)
    forehand_side_wall: float = Field(default=BASE_SKILL_NEW)
    backhand_side_wall: float = Field(default=BASE_SKILL_NEW)
    forehand_double_walls: float = Field(default=BASE_SKILL_NEW)
    backhand_double_walls: float = Field(default=BASE_SKILL_NEW)
    forehand_counter_wall: float = Field(default=BASE_SKILL_NEW)
    backhand_counter_wall: float = Field(default=BASE_SKILL_NEW)
    forehand_volley: float = Field(default=BASE_SKILL_NEW)
    backhand_volley: float = Field(default=BASE_SKILL_NEW)
    lob: float = Field(default=BASE_SKILL_NEW)
    smash: float = Field(default=BASE_SKILL_NEW)
    bandeja: float = Field(default=BASE_SKILL_NEW)



# Properties to receive on item update
class PadelStrokeUpdate(PadelStrokeCreate):
    pass


# Database model, database table inferred from class name
class PadelStroke(PadelStrokeBase, table=True):
    __tablename__ = "padel_strokes_skill_table"
    user_public_id: uuid.UUID = Field(primary_key=True)


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


    def update_from_paddle_stroke_create(self, info: PadelStrokeCreate):
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

    def generate_padel_strok_public(self):
        public = PadelStrokePublic(user_public_id=self.user_public_id)
        for field in self.__dict__:
            if field == "user_public_id" or field[0] == "_":
                continue
            value = getattr(self, field)
            setattr(public, field, self.skill_categorization(value))
        return public


# Properties to return via API, id is always required
class PadelStrokePublic(PadelStrokeCreate):
    user_public_id: uuid.UUID = Field(primary_key=True)

