from uuid import UUID

from app.models.player import Player, PlayerCreate, PlayerUpdate
from app.repository.players_repository import PlayersRepository
from app.services.strokes_service import StrokesService
from app.services.google_service import GoogleService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class PlayersService:

    async def create_player(
        self, session: SessionDep, player_in: PlayerCreate
    ) -> Player:
        # auxiliary_service_strokes = StrokesService()
        repo = PlayersRepository(session)
        # try:
        #     _stroke = await auxiliary_service_strokes.create_padel_stroke(session, None, player_in.user_public_id)
        # except NotUniqueException:
        #     raise NotUniqueException("player")
        # except Exception as e:
        #     raise e
        player = await repo.create_player(player_in)
        # session.close()
        return player

    async def update_player(
        self, session: SessionDep, user_public_id: UUID, player_in: PlayerUpdate
    ) -> Player:
        if player_in.zone_location:
            service = GoogleService()
            longitude, latitude = await service.get_coordinates(player_in.zone_location)
            player_in.longitude = longitude
            player_in.latitude = latitude
        repo = PlayersRepository(session)
        return await repo.update_player(user_public_id, player_in)

    async def read_player(self, session: SessionDep, user_public_id: UUID) -> Player:
        repo = PlayersRepository(session)
        return await repo.get_player_by_user_public_id(user_public_id)
