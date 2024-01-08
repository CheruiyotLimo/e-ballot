from .db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, LargeBinary
from sqlalchemy.sql.expression import text, null


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, nullable=False, primary_key=True)
    reg_num = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text("now()"))
    first_choice = Column(Integer, ForeignKey("hosp.id", ondelete="CASCADE"), nullable=True)
    second_choice = Column(Integer, ForeignKey("hosp.id", ondelete="CASCADE"), nullable=True)
    role = Column(String)
    posted = Column(Boolean, default=False)

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
    email = Column(String, nullable= False, unique=True)
    hosp_name = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    qrcode = Column(LargeBinary)
    
class AnalysisTble(Base):
    __tablename__='analysistable'
    
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable= False, unique=True)
    first_choice = Column(Integer, ForeignKey("hosp.id", ondelete="CASCADE"), nullable=True)
    second_choice = Column(Integer, ForeignKey("hosp.id", ondelete="CASCADE"), nullable=True)
    alloc_hosp = Column(Integer, ForeignKey("hosp.id", ondelete="CASCADE"), nullable=False)