from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.player_availability import (
    PlayerAvailability,
    PlayerAvailabilityCreate,
    PlayerAvailabilityPublic,
)
from app.utilities.exceptions import NotUniqueException


class PlayersAvailabilityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _commit_with_exception_handling(self):
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if "uq_player_availability_constraint" in str(e.orig):
                raise NotUniqueException("player availability")
            else:
                raise e

    async def create_player_availability(
        self, user_public_id: UUID, player_availability_in: PlayerAvailabilityCreate
    ) -> PlayerAvailabilityPublic:
        player_availability_create = PlayerAvailabilityCreate.model_validate(
            player_availability_in
        )
        available_days = player_availability_create.available_days
        for availability_day in range(1, 8):
            if availability_day in player_availability_create.available_days:
                player_availability = PlayerAvailability(
                    user_public_id=user_public_id,
                    week_day=availability_day,
                    is_available=True,
                )
            else:
                player_availability = PlayerAvailability(
                    user_public_id=user_public_id,
                    week_day=availability_day,
                    is_available=False,
                )
            self.session.add(player_availability)
        await self._commit_with_exception_handling()
        return PlayerAvailabilityPublic(
            user_public_id=user_public_id, available_days=available_days
        )
