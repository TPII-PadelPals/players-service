import uuid
from app.models.strokes import StrokeCreate, Stroke


def test_create_strokes() -> None:
    user_id = uuid.uuid4()
    create = StrokeCreate(serve=3.0)
    # test
    result = create.create_stroke_skill(user_id)
    # assert
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_" or field == "id":
            continue
        if field == "serve":
            assert value == 3.0
        elif field == "user_public_id":
            assert value == user_id
        else:
            assert value == 1.0


def test_skill_categorization_value() -> None:
    test_intermediate = 2
    test_advancance = 3
    for i in range(-10, test_intermediate):
        skill_value_less_2: float = i / 10.0
        assert Stroke.skill_categorization_value(skill_value_less_2) == 0
    for i in range(10 * test_intermediate, 10 * test_advancance):
        skill_value_upper_2_and_less_3: float = i / 10.0
        assert Stroke.skill_categorization_value(skill_value_upper_2_and_less_3) == 1
    for i in range(10 * test_advancance, 10 * (test_advancance + 1)):
        skill_value_upper_3: float = i / 10.0
        assert Stroke.skill_categorization_value(skill_value_upper_3) == 2


def test_generate_padel_strok_public() -> None:
    user_id = uuid.uuid4()
    create = StrokeCreate(serve=3.0, backhand_double_walls=2.0)
    stroke = create.create_stroke_skill(user_id)
    # test
    result = stroke.generate_stroke_public()
    # assert
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_":
            continue
        if field == "serve":
            assert value == 3.0
        elif field == "backhand_double_walls":
            assert value == 2.0
        elif field == "user_public_id":
            assert value == user_id
        else:
            assert value == 1.0
