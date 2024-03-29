from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config
from config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


database = Database(
    DB_URL,
    force_rollback=config.ENVIRONMENT == "TESTING",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
