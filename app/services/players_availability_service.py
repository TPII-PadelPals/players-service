from uuid import UUID

from app.models.player_availability import (
    PlayerAvailabilityList,
    PlayerAvailabilityListUpdate,
)
from app.repository.players_availability_repository import PlayersAvailabilityRepository
from app.utilities.dependencies import SessionDep


class PlayersAvailabilityService:
    async def create_player_availability(
        self,
        session: SessionDep,
        user_public_id: UUID,
    ) -> PlayerAvailabilityList:
        repo = PlayersAvailabilityRepository(session)
        player_availability = await repo.create_player_availability(user_public_id)
        return player_availability

    async def update_player_availability(
        self,
        session: SessionDep,
        user_public_id: UUID,
        player_availability_in: PlayerAvailabilityListUpdate,
    ) -> PlayerAvailabilityList:
        repo = PlayersAvailabilityRepository(session)
        return await repo.update_player_availability(
            user_public_id, player_availability_in
        )
