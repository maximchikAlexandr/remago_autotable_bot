from sqlalchemy import Column, Integer, String, Index, CheckConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    phone_number = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    user_id = Column(Integer, nullable=False)
    register_sign = Column(String, nullable=False, unique=True)
    car_year = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint("LENGTH(register_sign) < 15", name="check_length"),
    )
