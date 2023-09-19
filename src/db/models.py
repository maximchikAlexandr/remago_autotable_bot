from sqlalchemy import CheckConstraint
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from src.bot.utils.validators import PATTERN_REGISTER_SIGN

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
        CheckConstraint("LENGTH(register_sign) = 7", name="check_length"),
        CheckConstraint(f"register_sign ~ '{PATTERN_REGISTER_SIGN}'",
                        name="check_sign_format"),
    )
