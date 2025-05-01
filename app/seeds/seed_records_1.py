import uuid
from typing import Any

from app.models import Player, PlayerAvailability
from app.models.player_availability import WeekDay


class PlayersPaseoColon:
    n_players = 3

    @classmethod
    def records(cls) -> list[Any]:
        return cls.players() + cls.players_availabilities()

    @classmethod
    def players(cls) -> list[Any]:
        players = [
            Player(
                user_public_id=uuid.uuid4(),
                search_range_km=10,
                address="Av. Paseo Colon 850, CABA",
                latitude=-34.617393884228775,
                longitude=-58.368213261883554,
                time_availability=1,
            )
            for _ in range(cls.n_players)
        ]
        return players

    @classmethod
    def players_availabilities(cls) -> list[Any]:
        players_avails = [
            PlayerAvailability(
                user_public_id=player.user_public_id,
                week_day=WeekDay.THURSDAY,
                is_available=True,
            )
            for player in cls.players()
        ]
        return players_avails


RECORDS: list[Any] = []
RECORDS += PlayersPaseoColon().records()
