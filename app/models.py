from .db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text, null


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False)
    reg_num = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text("now()"))