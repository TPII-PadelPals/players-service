from collections.abc import Callable, Coroutine
from typing import Any, NoReturn

from app.utilities.exceptions import NotUniqueException


def mock_raise_not_unique_exception(
    class_name: str,
) -> Callable[..., Coroutine[Any, Any, NoReturn]]:
    async def _raise(*_args: Any, **_kwargs: Any) -> NoReturn:
        raise NotUniqueException(class_name)

    return _raise
