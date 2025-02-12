from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player_availability import (
    PlayerAvailability,
    PlayerAvailabilityPublic,
)
from app.utilities.repository.players_utils import PlayersUtils


class PlayersAvailabilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_player_availability(
        self, user_public_id: UUID
    ) -> PlayerAvailabilityPublic:
        player_availabilities = []
        for availability_day in PlayerAvailability.range_valids_day():
            player_availability = PlayerAvailability(
                user_public_id=user_public_id, week_day=availability_day
            )
            player_availabilities.append(player_availability.model_dump())
            self.session.add(player_availability)
        await PlayersUtils(self.session).flush_with_exception_handling(
            constraint_name="uq_player_availability_constraint",
            class_name="player availability",
        )
        return PlayerAvailabilityPublic(available_days=player_availabilities)
