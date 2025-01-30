import uuid
from sqlmodel import Field, SQLModel


# Properties to receive on item creation
class PadelStrokeCreate(SQLModel):
    serve: str
    forehand_ground: str
    background_ground: str
    forehand_back_wall: str
    backhand_back_wall: str
    forehand_side_wall: str
    backhand_side_wall: str
    forehand_double_walls: str
    backhand_double_walls: str
    forehand_counter_wall: str
    backhand_counter_wall: str
    forehand_volley: str
    backhand_volley: str
    lob: str
    smash: str
    bandeja: str

    def create_padel_stroke_skill(self, player_id: str):
        result = PadelStrokeBase(
            player_id=player_id,
            serve=1.0,
            forehand_ground=1.0,
            background_ground=1.0,
            forehand_back_wall=1.0,
            backhand_back_wall=1.0,
            forehand_side_wall=1.0,
            backhand_side_wall=1.0,
            forehand_double_walls=1.0,
            backhand_double_walls=1.0,
            forehand_counter_wall=1.0,
            backhand_counter_wall=1.0,
            forehand_volley=1.0,
            backhand_volley=1.0,
            lob=1.0,
            smash=1.0,
            bandeja=1.0
        )
        result.update_from_paddle_stroke_create(self)
        return result


# Shared properties
class PadelStrokeBase(SQLModel):
    serve: float = Field(default=1.0)
    forehand_ground: float = Field(default=1.0)
    background_ground: float = Field(default=1.0)
    forehand_back_wall: float = Field(default=1.0)
    backhand_back_wall: float = Field(default=1.0)
    forehand_side_wall: float = Field(default=1.0)
    backhand_side_wall: float = Field(default=1.0)
    forehand_double_walls: float = Field(default=1.0)
    backhand_double_walls: float = Field(default=1.0)
    forehand_counter_wall: float = Field(default=1.0)
    backhand_counter_wall: float = Field(default=1.0)
    forehand_volley: float = Field(default=1.0)
    backhand_volley: float = Field(default=1.0)
    lob: float = Field(default=1.0)
    smash: float = Field(default=1.0)
    bandeja: float = Field(default=1.0)


    def update_from_paddle_stroke_create(self, info: PadelStrokeCreate):
        for field in self.__dict__:
            value = getattr(info, field, None)
            if value is not None:
                setattr(self, field, self.transform(value))



# Properties to receive on item update
class PadelStrokeUpdate(PadelStrokeBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Database model, database table inferred from class name
class PadelStroke(PadelStrokeBase, table=True):
    __tablename__ = "items"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(nullable=False, index=True)


# Properties to return via API, id is always required
class PadelStrokePublic(PadelStrokeBase):
    player_id: str = Field(primary_key=True)


class ItemsPublic(SQLModel):
    data: list[PadelStrokePublic]
    count: int
