from app.utilities.exceptions import NotUniqueException


def mock_raise_not_unique_exception(class_name: str):
    async def _raise(*_args, **_kwargs):
        raise NotUniqueException(class_name)

    return _raise
