from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from enum import Enum





class UserTypeEnum(str, Enum):
    SUPER_ADMIN = "Super Admin"
    ORGIST_ADMIN = "Orgist Admin"
    ORGIST_USER = "Orgist User"
    USER = "User" 


class TimezoneEnum(str, Enum):
    UTC = "UTC"
    ASIA_KOLKATA = "Asia/Kolkata"
    US_EASTERN = "US/Eastern"
    US_CENTRAL = "US/Central"
    US_PACIFIC = "US/Pacific"
    EUROPE_LONDON = "Europe/London"
    EUROPE_BERLIN = "Europe/Berlin"
    AUSTRALIA_SYDNEY = "Australia/Sydney"
    ASIA_TOKYO = "Asia/Tokyo"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_uc = Column(String(15), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_email_verified = Column(Boolean, default=False)
    phone_number = Column(String, nullable=False)  
    is_phone_verified = Column(Boolean, default=False)
    password_hash = Column(Text, nullable=False)
    user_type = Column(String(50), nullable=False)
    orgist_id = Column(Integer, ForeignKey("orgist.id"), nullable=True)
    user_level = Column(Integer, nullable=False)
    timezone = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    org = relationship("Orgist", back_populates="users")
