import uuid

from app.models.strokes import StrokeCreate


def test_create_strokes() -> None:
    user_id = uuid.uuid4()
    create = StrokeCreate(serve=3.0)
    # test
    result = create.from_public(user_id)
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


def test_generate_padel_strok_public() -> None:
    user_id = uuid.uuid4()
    create = StrokeCreate(serve=3.0, backhand_double_walls=2.0)
    stroke = create.from_public(user_id)
    # test
    result = stroke.to_public()
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
