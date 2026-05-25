import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")  
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")


url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)


def get_engine():
    return engine

def get_session():
    return SessionLocal()
