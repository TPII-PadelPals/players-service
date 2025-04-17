from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"{item.capitalize()} not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotAuthorizedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )


class NotEnoughPermissionsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )


class NotUniqueException(HTTPException):
    def __init__(self, item: str) -> None:
        detail = f"{item.capitalize()} already exists."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ExternalServiceException(HTTPException):
    def __init__(self, service_name: str, detail: str) -> None:
        detail = f"EXT_SERVICE:{service_name}:{detail}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
