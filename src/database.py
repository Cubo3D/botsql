from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models import Base

_engine = create_engine(url="sqlite:///registry.db")
_sessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)
Base.metadata.create_all(_engine)


@contextmanager
def get_session():
    with _sessionLocal() as session:
        with session.begin():
            yield session


if __name__ == "__main__":
    with get_session() as session:
        result = session.execute(text("SELECT 1"))
        if result:
            print("database is online!")
