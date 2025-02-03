import uuid

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.strokes import Stroke, StrokePublic, StrokeCreate
from app.utilities.exceptions import NotFoundException, NotUniqueException


class StrokesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def _commit_with_exception_handling(self):
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise NotUniqueException("Padel strokes")


    async def get_strokes(self, user_public_id: uuid.UUID) -> StrokePublic:
        query = select(Stroke).where(Stroke.user_public_id == user_public_id)
        result = await self.session.exec(query)
        strokes: Stroke = result.first()
        if not strokes:
            raise NotFoundException(item="Padel strokes")
        return strokes.generate_stroke_public()


    async def create_stroke(self, stroke_in: StrokeCreate, user_public_id: uuid.UUID) -> Stroke:
        stroke_to_valid = stroke_in.create_stroke_skill(user_public_id)
        stroke = Stroke.model_validate(stroke_to_valid)
        self.session.add(stroke)
        await self._commit_with_exception_handling()
        await self.session.refresh(stroke)
        return stroke


    async def update_strokes(self, stroke_in: StrokeCreate, user_public_id: uuid.UUID) -> StrokePublic:
        query = select(Stroke).where(Stroke.user_public_id == user_public_id)
        result = await self.session.exec(query)
        strokes: Stroke = result.first()
        if not strokes:
            raise NotFoundException(item="Padel strokes")
        strokes.update_from_stroke_create(stroke_in)
        # update_dict = stroke_in.model_dump(exclude_unset=True)
        # strokes.sqlmodel_update(update_dict)
        self.session.add(strokes)
        await self.session.commit()
        await self.session.refresh(strokes)
        return strokes.generate_stroke_public()
