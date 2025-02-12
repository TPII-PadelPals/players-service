import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player import PlayerCreate
from app.services.players_service import PlayersService


async def test_create_player_service(session: AsyncSession) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    player_service = PlayersService()
    player_create = PlayerCreate(user_public_id=user_public_id, telegram_id=telegram_id)

    player = await player_service.create_player(session, player_create)
    await session.commit()
    await session.refresh(player)

    assert player.user_public_id == player_create.user_public_id
    assert player.telegram_id == player_create.telegram_id
    assert player.search_range_km is None
    assert player.address is None
    assert player.latitude is None
    assert player.longitude is None
    assert player.time_availability is None
