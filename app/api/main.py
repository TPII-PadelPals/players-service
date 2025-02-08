from fastapi import APIRouter

from app.api.routes import items, items_service, players, strokes

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(strokes.router, prefix="/players/{user_public_id}/strokes", tags=["strokes"])
