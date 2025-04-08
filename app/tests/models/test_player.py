from app.models.player import PlayerBase


def test_time_availability_sets() -> None:
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[1]
        for time_avail in [1, 4, 5, 7]
    )
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[2]
        for time_avail in [2, 4, 6, 7]
    )
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[3]
        for time_avail in [3, 5, 6, 7]
    )
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[4]
        for time_avail in [1, 2, 4, 5, 6, 7]
    )
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[5]
        for time_avail in [1, 3, 4, 5, 6, 7]
    )
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[6]
        for time_avail in [2, 3, 4, 5, 6, 7]
    )
    assert all(
        time_avail in PlayerBase.TIME_AVAILABILITY_SETS[7]
        for time_avail in [1, 2, 3, 4, 5, 6, 7]
    )
