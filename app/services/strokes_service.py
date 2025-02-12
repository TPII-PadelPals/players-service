import uuid

from app.models.strokes import Stroke, StrokeCreate, StrokePublic, StrokeUpdate
from app.repository.strokes_repository import StrokesRepository
from app.utilities.dependencies import SessionDep


class StrokesService:
    async def get_strokes(
        self, session: SessionDep, user_public_id: uuid.UUID
    ) -> StrokePublic:
        repo = StrokesRepository(session)
        stroke = await repo.get_strokes(user_public_id)
        return stroke.to_public()

    async def create_strokes(
        self,
        session: SessionDep,
        stroke_in: StrokeCreate | None,
        user_public_id: uuid.UUID,
    ) -> Stroke:
        repo = StrokesRepository(session)
        if stroke_in is None:
            stroke_in = StrokeCreate()
        return await repo.create_strokes(stroke_in, user_public_id)

    async def update_strokes(
        self,
        session: SessionDep,
        user_public_id: uuid.UUID,
        stroke_in: StrokeUpdate,
    ) -> StrokePublic:
        repo = StrokesRepository(session)
        stroke = await repo.update_strokes(stroke_in, user_public_id)
        return stroke.to_public()
