from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.db.orm import Base
from infrastructure.config import DB_URL


engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
