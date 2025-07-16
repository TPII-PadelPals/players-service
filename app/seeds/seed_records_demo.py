from typing import Any

from app.models import Player, PlayerAvailability
from app.models.player_availability import WeekDay
from app.models.strokes import Stroke

USER_2_UUID = "db08d286-58cf-4542-8501-efa273e38be4"


class PlayerSeed:
    def __init__(
        self,
        user_public_id: str,
        search_range_km: int,
        address: str,
        latitude: float,
        longitude: float,
        time_availability: int,
        week_day: WeekDay,
    ) -> None:
        self.player = self._init_player(
            user_public_id,
            search_range_km,
            address,
            latitude,
            longitude,
            time_availability,
        )
        self.player_avail = self._init_player_avail(user_public_id, week_day)
        self.strokes = self._init_strokes(user_public_id)

    def _init_player(
        self,
        user_public_id: str,
        search_range_km: int,
        address: str,
        latitude: float,
        longitude: float,
        time_availability: int,
    ) -> Any:
        return Player(
            user_public_id=user_public_id,
            search_range_km=search_range_km,
            address=address,
            latitude=latitude,
            longitude=longitude,
            time_availability=time_availability,
        )

    def _init_player_avail(self, user_public_id: str, week_day: WeekDay) -> Any:
        return PlayerAvailability(
            user_public_id=user_public_id,
            week_day=week_day,
            is_available=True,
        )

    def _init_strokes(self, user_public_id: str) -> Any:
        return Stroke(user_public_id=user_public_id)

    def records(self) -> list[Any]:
        return [self.player, self.player_avail, self.strokes]


RECORDS: list[Any] = []
RECORDS += PlayerSeed(
    user_public_id=USER_2_UUID,
    search_range_km=10,
    address="Av. Paseo Colon 300, CABA",
    latitude=-34.60973318891368,
    longitude=-58.36792940183134,
    time_availability=1,
    week_day=WeekDay.SATURDAY,
).records()
