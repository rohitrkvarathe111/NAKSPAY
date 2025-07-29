from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey, Date, JSON
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


class IdentityTypeEnum(str, Enum):
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    AADHAAR = "aadhaar"
    PAN = "pan"
    VOTER_ID = "voter_id"
    GREEN_CARD = "green_card"

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


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




class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    profile_img = Column(String(150), nullable=True)
    identity_type = Column(String(50), nullable=True)
    identity_no = Column(String(70), nullable=True)
    identity_img = Column(String(150), nullable=True)
    identity_verified = Column(Boolean, default=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(String(150), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    pincode = Column(Integer, nullable=True)
    website = Column(String(150), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    role = Column(String(150), nullable=True)
    preferences = Column(JSON, nullable=True)
