from fastapi import status

from app.utilities.exceptions import ExternalServiceException

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

PLAYERS_PATCH_500_RESPONSES = {
    "description": "",
    "content": {
        "application/json": {
            "examples": {
                "Google invalid address": {
                    "value": {
                        "detail": ExternalServiceException(
                            service_name="google-address", detail="Invalid location"
                        ).detail,
                    },
                },
                "Google failed to fetch": {
                    "value": {
                        "detail": ExternalServiceException(
                            service_name="google-address",
                            detail="Failed to fetch coordinates from Google",
                        ).detail,
                    },
                },
            }
        }
    },
}

PLAYERS_PATCH_RESPONSES = {
    status.HTTP_200_OK: {"description": "Player updated"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: PLAYERS_PATCH_500_RESPONSES,
    **PLAYER_NOT_FOUND,
}

PLAYERS_GET_RESPONSES = {**PLAYER_NOT_FOUND}

STROKES_NOT_FOUND = {
    status.HTTP_404_NOT_FOUND: {"description": "Padel strokes not found."}
}

STROKES_PUT_RESPONSES = {
    status.HTTP_200_OK: {"description": "Player strokes updated"},
    **STROKES_NOT_FOUND,
}

STROKES_GET_RESPONSES = {**STROKES_NOT_FOUND}
