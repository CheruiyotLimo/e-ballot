from .db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text, null


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False, primary_key=True)
    reg_num = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text("now()"))
    choice = Column(Integer, ForeignKey("hosp.id", ondelete="CASCADE"), nullable=True)
    role = Column(String)

class Hospital(Base):
    __tablename__ = "hosp"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    county_name = Column(String, nullable=False)
    county_num = Column(Integer, nullable=False)
    slots = Column(Integer, nullable=False)

class AssignedHosp(Base):
    __tablename__="hospassign"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    hosp_name = Column(String, nullable=False)