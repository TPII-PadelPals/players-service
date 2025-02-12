from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utilities.exceptions import NotUniqueException


class PlayersUtils:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def flush_with_exception_handling(
        self, constraint_name: str, class_name: str
    ) -> None:
        try:
            await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            if constraint_name in str(e.orig):
                raise NotUniqueException(class_name)
            else:
                raise e
