from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#still need to abstract the specifics
db_url = "postgresql://postgres:password@localhost:5432/ballot"

engine = create_engine(db_url) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close() 


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Succesful connection.")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print(error)
#         time.sleep(2)