import uuid

from app.models.padel_stroke import PadelStrokeCreate, PadelStrokeUpdate
from app.utilities.dependencies import SessionDep


class PadelStrokesService:
    async def get_padel_strokes(self, user_public_id: uuid.UUID):
        pass


    async def create_padel_stroke(self, session: SessionDep, padel_stroke_in: PadelStrokeCreate):
        pass


    async def update_padel_stroke(
            self,
            session: SessionDep,
            user_public_id: uuid.UUID,
            padel_stroke_in: PadelStrokeUpdate,
    ):
        pass