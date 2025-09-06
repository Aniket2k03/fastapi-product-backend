from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)