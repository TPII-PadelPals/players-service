from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.utilities.exceptions import NotUniqueException


async def mock_create_player_availability_raise_not_unique_exception(
    _self: Any, _session: AsyncSession, _user_public_id: str
) -> None:
    mock_raise_not_unique_exception("player availability")


def mock_raise_not_unique_exception(class_name: str) -> None:
    raise NotUniqueException(class_name)
