from sqlalchemy import select
from database import get_session
from models import User


def get_user(id: int):
    with get_session() as session:
        stmt = select(User).where(User.userid == id)
        result = session.execute(stmt).scalar_one_or_none()
        return result


def create_user(name: str | None, id: int):
    with get_session() as session:
        user = User(username=name, userid=id)
        session.add(user)
        return user
