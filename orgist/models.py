from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Date, Text, JSON
from database import Base
from sqlalchemy.orm import relationship





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
    user_mappings = relationship("UserMapping", foreign_keys="[UserMapping.orgist_id]", back_populates="orgist")
    mapped_mappings = relationship("UserMapping", foreign_keys="[UserMapping.mapped_orgist_id]", back_populates="mapped_orgist")



class OrgistProfile(Base):
    __tablename__ = "orgist_profile"

    id = Column(Integer, primary_key=True, index=True)
    orgist_id = Column(Integer, ForeignKey("orgist.id"), nullable=False)
    org_uc = Column(String(15), nullable=False)
    org_add = Column(String(150), nullable=True)
    org_city = Column(String(50), nullable=True)
    org_state = Column(String(50), nullable=True)
    org_pin = Column(Integer, nullable=True)
    org_country = Column(String(50), nullable=True)
    org_web = Column(String(100), nullable=True)
    org_owner = Column(String(50), nullable=True)
    org_est_date = Column(Date, nullable=True)
    org_GSTIN = Column(String(70), nullable=True)
    GSTIN_img = Column(String(150), nullable=True)
    org_LLPIN = Column(String(70), nullable=True)
    LLPIN_img = Column(String(150), nullable=True)
    org_CIN = Column(String(70), nullable=True)
    CIN_img = Column(String(150), nullable=True)
    org_PAN = Column(String(70), nullable=True)
    PAN_img = Column(String(150), nullable=True)
    org_logo = Column(String(150), nullable=True)
    remarks = Column(Text, nullable=True)
    other_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    orgist = relationship("Orgist", backref="profile")
    created_user = relationship("User", foreign_keys=[created_by])
    updated_user = relationship("User", foreign_keys=[updated_by])
