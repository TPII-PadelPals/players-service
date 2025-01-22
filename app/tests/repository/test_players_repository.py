import uuid

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player import PlayerCreate, PlayerUpdate
from app.repository.players_repository import PlayersRepository
from app.utilities.exceptions import NotFoundException, NotUniqueException


async def test_create_player(session: AsyncSession) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    repo = PlayersRepository(session)
    player_create = PlayerCreate(user_public_id=user_public_id, telegram_id=telegram_id)

    player = await repo.create_player(player_create)

    assert player.user_public_id == player_create.user_public_id
    assert player.telegram_id == player_create.telegram_id
    assert player.zone_km is None
    assert player.zone_location is None
    assert player.latitude is None
    assert player.longitude is None
    assert player.time_availability is None


async def test_create_player_with_user_public_id_already_exists_raises_exception(
    session: AsyncSession,
) -> None:
    repo = PlayersRepository(session)

    user_public_id = uuid.uuid4()
    duplicated_user_p_id = user_public_id

    player_create = PlayerCreate(user_public_id=user_public_id, telegram_id=30304040)

    await repo.create_player(player_create)

    with pytest.raises(NotUniqueException) as e:
        player_create = PlayerCreate(
            user_public_id=duplicated_user_p_id, telegram_id=50509090
        )
        await repo.create_player(player_create)

    assert e.value.detail == "Player already exists."


async def test_update_player(session: AsyncSession) -> None:
    user_public_id = str(uuid.uuid4())
    telegram_id = 10103030

    repo = PlayersRepository(session)
    player_create = PlayerCreate(user_public_id=user_public_id, telegram_id=telegram_id)

    player = await repo.create_player(player_create)

    time_availability = 5

    player_update = PlayerUpdate(time_availability=time_availability)

    updated_player = await repo.update_player(player.user_public_id, player_update)

    assert updated_player.user_public_id == player.user_public_id
    assert updated_player.telegram_id == player.telegram_id
    assert updated_player.time_availability == time_availability
    assert updated_player.zone_km == player.zone_km
    assert updated_player.zone_location == player.zone_location
    assert updated_player.latitude == player.latitude
    assert updated_player.longitude == player.longitude


async def test_update_player_with_not_found_player_returns_exception(
    session: AsyncSession,
) -> None:
    repo = PlayersRepository(session)

    time_availability = 5
    user_public_id_not_found = uuid.uuid4()

    with pytest.raises(NotFoundException) as e:
        player_update = PlayerUpdate(time_availability=time_availability)
        await repo.update_player(user_public_id_not_found, player_update)

    assert e.value.detail == "Player not found."
