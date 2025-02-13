import uuid

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.players_availability_service import PlayersAvailabilityService
from app.utilities.exceptions import NotUniqueException


async def test_create_player_availability_days_are_all_unavailable(
    session: AsyncSession,
) -> None:
    user_public_id = uuid.uuid4()
    expected_player_availabilities = [
        {"user_public_id": user_public_id, "week_day": i, "is_available": False}
        for i in range(1, 8)
    ]
    player_availability_service = PlayersAvailabilityService()

    player_availability = await player_availability_service.create_player_availability(
        session, user_public_id
    )
    await session.commit()
    for player_availabilities in player_availability.available_days:
        await session.refresh(player_availabilities)

    assert len(player_availability.available_days) == len(
        expected_player_availabilities
    )

    actual_availabilities = [
        {
            "user_public_id": day.user_public_id,
            "week_day": day.week_day,
            "is_available": day.is_available,
        }
        for day in player_availability.available_days
    ]

    assert (
        actual_availabilities == expected_player_availabilities
    ), f"Expected: {expected_player_availabilities}, but got: {actual_availabilities}"


async def test_create_player_available_days_user_public_id_already_exists_returns_error(
    session: AsyncSession,
) -> None:
    user_public_id = uuid.uuid4()

    player_availability_service = PlayersAvailabilityService()

    _player_availability = await player_availability_service.create_player_availability(
        session, user_public_id
    )
    await session.commit()

    with pytest.raises(NotUniqueException) as e:
        _duplicated_player_availability = (
            await player_availability_service.create_player_availability(
                session, user_public_id
            )
        )
        await session.commit()
    assert e.value.detail == "Player availability already exists."
