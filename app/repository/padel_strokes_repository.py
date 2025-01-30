import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.padel_stroke import PadelStroke, PadelStrokePublic, PadelStrokeCreate
from app.utilities.exceptions import NotFoundException


class PadelStrokesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get_padel_strokes(self, user_public_id: uuid.UUID) -> PadelStrokePublic:
        query = select(PadelStroke).where(PadelStroke.user_public_id == user_public_id)
        result = await self.session.exec(query)
        strokes: PadelStroke = result.first()
        if not strokes:
            raise NotFoundException(item="Padel strokes not found")
        return strokes.generate_padel_strok_public()


    async def create_padel_strokes(self, padel_stroke_in: PadelStrokeCreate, user_public_id: uuid.UUID) -> PadelStroke:
        stroke_to_valid = padel_stroke_in.create_padel_stroke_skill(user_public_id)
        stroke = PadelStroke.model_validate(stroke_to_valid)
        self.session.add(stroke)
        await self.session.commit()
        await self.session.refresh(stroke)
        return stroke