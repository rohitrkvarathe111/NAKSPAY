from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base
from enum import Enum
from sqlalchemy.orm import relationship



class OrgCateEnum(str, Enum):
    COMPANY = "Company"
    GOVERNMENT_OFFICE = "Government Office"
    PG = "PG (Paying Guest Accommodation)"
    HOTEL = "Hotel"
    MALL = "Mall"
    CLINIC = "Clinic"
    SCHOOL = "School"


class OrgTypeEnum(str, Enum):
    PRIVATE = "Private Organization"
    PUBLIC = "Public Organization"
    GOVERNMENT = "Government Body"
    NGO = "Non-Governmental Organization"
    NON_PROFIT = "Non-Profit Organization"
    STARTUP = "Startup"
    MNC = "Multinational Corporation"
    EDUCATIONAL = "Educational Institution"
    HEALTHCARE = "Healthcare Organization"
    FINANCIAL = "Financial Institution"

class OrgIDTypeEnum(str, Enum):
    PAN = "Permanent Account Number"
    GST = "Goods and Services Tax Identification Number"
    CIN = "Corporate Identification Number"
    TAN = "Tax Deduction and Collection Account Number"
    MSME = "Micro, Small and Medium Enterprises Registration"
    UDYAM = "Udyam Registration"
    NGO_DARPAN = "NGO Darpan ID"
    FCRA = "Foreign Contribution Regulation Act Number"
    LLPIN = "Limited Liability Partnership Identification Number"





class Orgist(Base):
    __tablename__ = "orgist"

    id = Column(Integer, primary_key=True, index=True)
    org_uc = Column(String(15), nullable=False, unique=True)
    org_name = Column(String(200), nullable=False)
    org_sort_name = Column(String(50), nullable=False)
    org_type = Column(String(100), nullable=False)
    org_cate = Column(String(100), nullable=False)
    org_email = Column(String(255), nullable=False, unique=True)
    org_mobile = Column(String(20), nullable=False)
    identity_type = Column(String(100), nullable=False)
    identity_code = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    org_high_level = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    users = relationship("User", back_populates="org")