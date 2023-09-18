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
        conn = engine_db.connect()
        self.connection = conn.execution_options(echo=True)
        self.model = self.MODEL_CLASS

    def create(
        self,
        user_id: int,
        phone_number: str,
        first_name: str,
        last_name: str,
        register_sign: str,
        car_year: int,
    ) -> None:
        query: Insert = insert(self.model).values(
            user_id=user_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            register_sign=register_sign,
            car_year=car_year,
        )
        self.connection.execute(query)
        self.connection.commit()

    def get_user_data_by_register_sign(self, register_sign: str) -> dict:
        query: Select = select(
            func.json_build_object(
                'user_id', self.model.user_id,
                'phone_number', self.model.phone_number,
                'first_name', self.model.first_name,
                'last_name', self.model.last_name
            ).label('user_data')
        ).where(self.model.register_sign == register_sign)
        result: Row = self.connection.execute(query).fetchone()
        return result.user_data

    def get_user_data_by_user_id(self, user_id: int) -> dict:
        query: Select = select(
            func.json_build_object(
                'phone_number', self.model.phone_number,
                'first_name', self.model.first_name,
                'last_name', self.model.last_name
            ).label('user_data')
        ).where(self.model.user_id == user_id)
        result: Row = self.connection.execute(query).fetchone()
        return result.user_data


    def is_existing_user(self, user_id: int) -> bool:
        query: Select = select(
            exists().where(self.model.user_id == user_id).label("is_existing_user")
        )
        result: Row = self.connection.execute(query).scalar()
        return result

    def is_existing_register_sign(self, register_sign: str) -> bool:
        query: Select = select(
            exists().where(self.model.register_sign == register_sign).label("is_existing_user")
        )
        result: Row = self.connection.execute(query).scalar()
        return result