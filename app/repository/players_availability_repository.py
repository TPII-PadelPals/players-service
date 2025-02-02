from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player_availability import (
    PlayerAvailability,
    PlayerAvailabilityCreate,
    PlayerAvailabilityPublic,
)
from app.repository.players_utils import PlayersUtils


class PlayersAvailabilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_player_availability(
        self, user_public_id: UUID, player_availability_in: PlayerAvailabilityCreate
    ) -> PlayerAvailabilityPublic:
        player_availability_create = PlayerAvailabilityCreate.model_validate(
            player_availability_in
        )
        available_days = player_availability_create.available_days
        for availability_day in range(1, 8):
            player_availability = PlayerAvailability(
                user_public_id=user_public_id, week_day=availability_day
            )
            availability_day in player_availability_create.available_days and player_availability.set_available()
            self.session.add(player_availability)
        await PlayersUtils(self.session).commit_with_exception_handling(
            constraint_name="uq_player_availability_constraint",
            class_name="player availability",
        )
        return PlayerAvailabilityPublic(
            user_public_id=user_public_id, available_days=available_days
        )
