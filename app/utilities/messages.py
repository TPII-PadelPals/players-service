from fastapi import status

# Common responses
NOT_ENOUGH_PERMISSIONS = {
    status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"}
}

# Item responses
ITEM_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Item not found."}}
ITEM_RESPONSES = {**ITEM_NOT_FOUND, **NOT_ENOUGH_PERMISSIONS}

# Player responses
PLAYER_ALREADY_EXISTS = {
    status.HTTP_409_CONFLICT: {"description": "User public id already exists."}
}
PLAYERS_POST_RESPONSES = {
    status.HTTP_201_CREATED: {"description": "Player created"},
    **PLAYER_ALREADY_EXISTS,
}

PLAYER_NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "Player not found."}}
PLAYERS_PUT_RESPONSES = {
    status.HTTP_200_OK: {"description": "Player updated"},
    **PLAYER_NOT_FOUND,
}
