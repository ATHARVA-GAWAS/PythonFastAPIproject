from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a sqlite engine instance
DATABASE_URL = "postgresql://postgres:postgres@localhost/apidatabase"
engine = create_engine(DATABASE_URL)

# Create a DeclarativeMeta instance
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

