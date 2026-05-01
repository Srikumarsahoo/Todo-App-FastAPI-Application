from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("RENDER_POSTGRES_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("RENDER_POSTGRES_URL is not set in the environment.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

Base = declarative_base()

# Sqlite3 path:
# 'sqlite:///./todosapp.db'

##postgresql://postgres_database_7qam_user:saRy9PPKzERQk0yQfiVNb6hIQlfJvQw4@dpg-d7potm8sfn5c73aalkog-a/postgres_database_7qam

##postgresql://postgres:test1234@localhost/postgres
