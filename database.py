from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session,sessionmaker,declarative_base
from sqlalchemy import create_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL,echo=True)
Base = declarative_base()
sessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

def get_db():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()


