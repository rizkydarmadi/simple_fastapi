from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import Settings

engine = create_engine(
    "postgresql+psycopg://postgres:12qwaszx@localhost:5432/test_code",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
