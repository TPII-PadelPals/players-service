import uuid
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player import Player, PlayerCreate, PlayerUpdate
from app.utilities.exceptions import NotFoundException, NotUniqueException


class PlayersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _check_unique_attr(self, attr: Any, value: Any) -> None:
        player_attr = getattr(Player, attr)
        statement = select(player_attr).where(player_attr == value)
        attr_exist = (await self.session.exec(statement)).first()
        if attr_exist:
            attr_str = " ".join(attr.split("_"))
            raise NotUniqueException(item=attr_str.capitalize())

    async def create_player(self, player_in: PlayerCreate) -> Player:
        player = Player.model_validate(player_in)
        await self._check_unique_attr("user_public_id", player.user_public_id)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def update_player(
        self, user_public_id: uuid.UUID, player_in: PlayerUpdate
    ) -> Player:
        query = select(Player).where(Player.user_public_id == user_public_id)
        result = await self.session.exec(query)
        player = result.first()
        if not player:
            raise NotFoundException(item="Player")
        update_dict = player_in.model_dump(exclude_unset=True)
        player.sqlmodel_update(update_dict)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player
