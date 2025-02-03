import uuid

from app.models.strokes import StrokeCreate, StrokeUpdate, StrokePublic
from app.repository.strokes_repository import StrokesRepository
from app.utilities.dependencies import SessionDep


class StrokesService:
    async def get_strokes(
            self,
            session: SessionDep,
            user_public_id: uuid.UUID
    ) -> StrokePublic:
        repo = StrokesRepository(session)
        return await repo.get_strokes(user_public_id)


    async def create_padel_stroke(
            self,
            session: SessionDep,
            stroke_in: StrokeCreate | None,
            user_public_id: uuid.UUID
    ):
        repo = StrokesRepository(session)
        if stroke_in is None:
            stroke_in = StrokeCreate()
        return await repo.create_stroke(stroke_in, user_public_id)


    async def update_stroke(
            self,
            session: SessionDep,
            user_public_id: uuid.UUID,
            stroke_in: StrokeUpdate,
    ):
        repo = StrokesRepository(session)
        return await repo.update_strokes(stroke_in, user_public_id)