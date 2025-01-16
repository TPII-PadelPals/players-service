from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player import Player, PlayerCreate


class PlayersRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # async def _check_unique_attr(self, attr: Any, value: Any) -> None:
    #     player_attr = getattr(Player, attr)
    #     statement = select(player_attr).where(player_attr == value)
    #     attr_exist = (await self.session.exec(statement)).first()
    #     if attr_exist:
    #         raise NotUniqueException(item=attr.capitalize())

    async def create_player(self, player_in: PlayerCreate) -> Player:
        player = Player.model_validate(player_in)
        # await self._check_unique_attr("email", player.email)
        # await self._check_unique_attr("phone", player.phone)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player
