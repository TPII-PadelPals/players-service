from app.utilities.exceptions import NotUniqueException


async def mock_raise_not_unique_exception(class_name):
    raise NotUniqueException(class_name)
