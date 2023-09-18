from sqlalchemy import (
    func,
    insert,
    select,
    exists,
)
from sqlalchemy.engine.row import Row
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.selectable import Select

from src.db.models import UserModel
from src.db.settings import EngineDB


class UserFacade:
    MODEL_CLASS = UserModel

    def __init__(self, engine_db: EngineDB) -> None:
        self.engine = engine_db.execution_options(echo=True)
        self.model = self.MODEL_CLASS

    async def create(
        self,
        user_id: int,
        phone_number: str,
        first_name: str,
        last_name: str,
        register_sign: str,
        car_year: int,
    ) -> None:
        async with self.engine.begin() as conn:
            query: Insert = insert(self.model).values(
                user_id=user_id,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                register_sign=register_sign,
                car_year=car_year,
            )
            await conn.execute(query)

    async def get_user_data_by_register_sign(self, register_sign: str) -> dict:
        async with self.engine.connect() as conn:
            query: Select = select(
                func.json_build_object(
                    "user_id",
                    self.model.user_id,
                    "phone_number",
                    self.model.phone_number,
                    "first_name",
                    self.model.first_name,
                    "last_name",
                    self.model.last_name,
                ).label("user_data")
            ).where(self.model.register_sign == register_sign)
            result: Row = await conn.execute(query)
            return result.fetchone().user_data

    async def get_user_data_by_user_id(self, user_id: int) -> dict:
        async with self.engine.connect() as conn:
            query: Select = select(
                func.json_build_object(
                    "phone_number",
                    self.model.phone_number,
                    "first_name",
                    self.model.first_name,
                    "last_name",
                    self.model.last_name,
                ).label("user_data")
            ).where(self.model.user_id == user_id)
            result: Row = await conn.execute(query)
            return result.fetchone().user_data

    async def is_existing_user(self, user_id: int) -> bool:
        async with self.engine.connect() as conn:
            query: Select = select(
                exists().where(self.model.user_id == user_id).label("is_existing_user")
            )
            result: Row = await conn.execute(query)
            return result.fetchone().is_existing_user

    async def is_existing_register_sign(self, register_sign: str) -> bool:
        async with self.engine.connect() as conn:
            query: Select = select(
                exists()
                .where(self.model.register_sign == register_sign)
                .label("is_existing_user")
            )
            result: Row = await conn.execute(query)
            return result.fetchone().is_existing_user
