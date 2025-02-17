from app.utilities.exceptions import NotUniqueException


async def mock_create_player_availability_raise_not_unique_exception(
    _self, _session, _user_public_id
):
    mock_raise_not_unique_exception("player availability")


def mock_raise_not_unique_exception(class_name):
    raise NotUniqueException(class_name)
