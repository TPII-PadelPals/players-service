import uuid

from app.models.padel_stroke import PadelStrokeCreate, PadelStrokeUpdate, PadelStrokePublic
from app.repository.padel_strokes_repository import PadelStrokesRepository
from app.utilities.dependencies import SessionDep


class PadelStrokesService:
    async def get_padel_strokes(
            self,
            session: SessionDep,
            user_public_id: uuid.UUID
    ) -> PadelStrokePublic:
        repo = PadelStrokesRepository(session)
        return await repo.get_padel_strokes(user_public_id)


    async def create_padel_stroke(
            self,
            session: SessionDep,
            padel_stroke_in: PadelStrokeCreate,
            user_public_id: uuid.UUID
    ):
        repo = PadelStrokesRepository(session)
        return await repo.create_padel_strokes(padel_stroke_in, user_public_id)


    async def update_padel_stroke(
            self,
            session: SessionDep,
            user_public_id: uuid.UUID,
            padel_stroke_in: PadelStrokeUpdate,
    ):
        repo = PadelStrokesRepository(session)
        return await repo.update_padel_strokes(padel_stroke_in, user_public_id)