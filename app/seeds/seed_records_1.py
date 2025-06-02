from typing import Any

from app.models import Player, PlayerAvailability
from app.models.player_availability import WeekDay
from app.models.strokes import Stroke

ASSIGNED_UUID = "db08d286-58cf-4542-8501-efa273e38be4"

SIMILAR_UUIDS = [
    "3cbccfa2-65d7-4d49-b801-b7f30daae857",
    "96ff36d6-bd6e-49c3-a666-cda2d2865be0",
    "a80a64fb-9672-450c-a98e-bcf366ea6ac8",
]


class PlayersPaseoColon:
    def __init__(self, players_uuids: list[str]) -> None:
        self.players = []
        self.players_avails = []
        self.strokes = []
        for player_uuid in players_uuids:
            self.players.append(
                Player(
                    user_public_id=player_uuid,
                    search_range_km=10,
                    address="Av. Paseo Colon 850, CABA",
                    latitude=-34.617393884228775,
                    longitude=-58.368213261883554,
                    time_availability=1,
                )
            )
            self.players_avails.append(
                PlayerAvailability(
                    user_public_id=player_uuid,
                    week_day=WeekDay.THURSDAY,
                    is_available=True,
                )
            )
            self.strokes.append(Stroke(user_public_id=player_uuid))

    def records(self) -> list[Any]:
        return self.players + self.players_avails + self.strokes


RECORDS: list[Any] = []
RECORDS += PlayersPaseoColon([ASSIGNED_UUID] + SIMILAR_UUIDS).records()
