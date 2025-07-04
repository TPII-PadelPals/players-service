from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player_availability import (
    PlayerAvailability,
    PlayerAvailabilityList,
    PlayerAvailabilityListUpdate,
)
from app.utilities.exceptions import NotFoundException
from app.utilities.repository.players_utils import PlayersUtils


class PlayersAvailabilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_player_availability(
        self, user_public_id: UUID
    ) -> PlayerAvailabilityList:
        player_availabilities = []
        for week_day in PlayerAvailability.valid_days():
            player_availability = PlayerAvailability(
                user_public_id=user_public_id, week_day=week_day
            )
            player_availabilities.append(player_availability)
            self.session.add(player_availability)
        await PlayersUtils(self.session).flush_with_exception_handling(
            constraint_name="uq_player_availability_constraint",
            class_name="player availability",
        )
        return PlayerAvailabilityList(
            user_public_id=user_public_id, available_days=player_availabilities
        )

    async def update_player_availability(
        self,
        user_public_id: UUID,
        player_availabilities_in: PlayerAvailabilityListUpdate,
    ) -> PlayerAvailabilityList:
        player_availabilities_updated = []

        query = select(PlayerAvailability).where(
            PlayerAvailability.user_public_id == user_public_id
        )
        player_availabilities = await self.session.exec(query)
        player_availabilities_list = player_availabilities.all()

        if not len(player_availabilities_list):
            raise NotFoundException(item="Player availability")

        for player_availability in player_availabilities_list:
            for player_availability_in in player_availabilities_in.available_days:
                if player_availability.week_day == player_availability_in.week_day:
                    update_dict = player_availability_in.model_dump(exclude_unset=True)
                    player_availability.sqlmodel_update(update_dict)
                    self.session.add(player_availability)
                    player_availabilities_updated.append(player_availability)
        await self.session.commit()

        for player_availability in player_availabilities_updated:
            await self.session.refresh(player_availability)

        return PlayerAvailabilityList(
            user_public_id=user_public_id, available_days=player_availabilities_updated
        )
