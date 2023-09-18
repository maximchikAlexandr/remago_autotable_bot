from sqlalchemy import CheckConstraint
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    register_sign: Mapped[str] = mapped_column(nullable=False, unique=True)
    car_year: Mapped[int] = mapped_column(nullable=False)
    __table_args__ = (
        CheckConstraint("LENGTH(register_sign) < 15", name="check_length"),
    )
