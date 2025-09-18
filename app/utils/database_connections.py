from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+psycopg2://myuser:123@localhost:5432/splitwise"  # Replace with your actual details

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()