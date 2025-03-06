import random
import string
import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.player import Player, PlayerCreate
from app.repository.players_repository import PlayersRepository


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_x_api_key_header() -> dict[str, str]:
    headers = {"x-api-key": f"{settings.API_KEY}"}
    return headers


async def create_player(session: AsyncSession, user_public_id: uuid.UUID) -> Player:
    user_public_id_str = str(user_public_id)
    repo = PlayersRepository(session)
    player_create = PlayerCreate(user_public_id=user_public_id_str)
    player = await repo.create_player(player_create)
    return player
