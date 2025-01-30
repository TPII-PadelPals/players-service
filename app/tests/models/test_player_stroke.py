import uuid
from app.models.padel_stroke import PadelStrokeCreate, DEFINITION_OF_CATEGORIZATION, BASE_ADVANCE, BASE_BEGINNER, \
    BASE_INTERMEDIATE, PadelStroke


def test_create_padel_stroke_skill():
    user_id = uuid.uuid4()
    create = PadelStrokeCreate(serve=DEFINITION_OF_CATEGORIZATION[2])
    # test
    result = create.create_padel_stroke_skill(user_id)
    # assert
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_":
            continue
        if field == "serve":
            assert value == BASE_ADVANCE
        elif field == "user_public_id":
            assert value == user_id
        else:
            assert value == BASE_BEGINNER


def test_skill_categorization_value():
    test_intermediate = int(BASE_INTERMEDIATE)
    test_advancance = int(BASE_ADVANCE)
    for i in range(-10, test_intermediate):
        skill_value: float = i / 10.0
        assert PadelStroke.skill_categorization_value(skill_value) == 0
    for i in range(10 * test_intermediate, 10 * test_advancance):
        skill_value: float = i / 10.0
        assert PadelStroke.skill_categorization_value(skill_value) == 1
    for i in range(10 * test_advancance, 10 * (test_advancance + 1)):
        skill_value: float = i / 10.0
        assert PadelStroke.skill_categorization_value(skill_value) == 2


def test_generate_padel_strok_public():
    user_id = uuid.uuid4()
    create = PadelStrokeCreate(serve=DEFINITION_OF_CATEGORIZATION[2], backhand_double_walls=DEFINITION_OF_CATEGORIZATION[1])
    stroke = create.create_padel_stroke_skill(user_id)
    # test
    result = stroke.generate_padel_strok_public()
    # assert
    for field in result.__dict__:
        value = getattr(result, field, None)
        if field[0] == "_":
            continue
        if field == "serve":
            assert value == DEFINITION_OF_CATEGORIZATION[2]
        elif field == "backhand_double_walls":
            assert value == DEFINITION_OF_CATEGORIZATION[1]
        elif field == "user_public_id":
            assert value == user_id
        else:
            assert value == DEFINITION_OF_CATEGORIZATION[0]


def test_separation_of_values():
    assert BASE_BEGINNER < BASE_INTERMEDIATE
    assert BASE_INTERMEDIATE < BASE_ADVANCE