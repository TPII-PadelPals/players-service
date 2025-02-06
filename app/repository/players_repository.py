from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player import Player, PlayerCreate, PlayerUpdate
from app.utilities.exceptions import NotFoundException, NotUniqueException


class PlayersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # async def _commit_with_exception_handling(self):
    #     try:
    #         await self.session.commit()
    #     except IntegrityError as e:
    #         await self.session.rollback()
    #         if "uq_player_constraint" in str(e.orig):
    #             raise NotUniqueException("player")
    #         else:
    #             raise e

    async def create_player(self, player_in: PlayerCreate) -> Player:
        player = Player.model_validate(player_in)
        self.session.add(player)
        # await self._commit_with_exception_handling()
        # await self.session.refresh(player)
        return player

    async def update_player(
        self, user_public_id: UUID, player_in: PlayerUpdate
    ) -> Player:
        player = await self.get_player_by_user_public_id(user_public_id=user_public_id)
        update_dict = player_in.model_dump(exclude_unset=True)
        player.sqlmodel_update(update_dict)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def get_player_by_user_public_id(self, user_public_id: UUID) -> Player:
        query = select(Player).where(Player.user_public_id == user_public_id)
        result = await self.session.exec(query)
        player = result.first()
        if not player:
            raise NotFoundException(item="Player")
        return player
