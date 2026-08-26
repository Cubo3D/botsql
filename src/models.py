from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "unregistered_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=True)
    userid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
