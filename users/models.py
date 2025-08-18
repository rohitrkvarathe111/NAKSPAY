from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey, Date, JSON
from database import Base
from sqlalchemy.orm import relationship



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

    user = relationship("User", backref="profile", foreign_keys=[user_id])



class Account(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    orgist_id = Column(Integer, ForeignKey("orgist.id"), nullable=True)
    full_name = Column(String(200), nullable=False)
    account_no = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", backref="account", foreign_keys=[user_id])
    orgist = relationship("Orgist", backref="account", foreign_keys=[orgist_id])
    



class UserMapping(Base):
    __tablename__ = "user_mapping"

    id = Column(Integer, primary_key=True, index=True)
    orgist_id = Column(Integer, ForeignKey("orgist.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    mapped_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    requested_by = Column(String(50), nullable=False)
    requested_user_id = Column(Integer, nullable=False)
    user_status = Column(String(50), nullable=False)
    map_user_status = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", foreign_keys=[user_id], backref="user_mappings")
    mapped_user = relationship("User", foreign_keys=[mapped_user_id], backref="mapped_mappings")
    created_by_user = relationship("User", foreign_keys=[created_by], backref="created_mappings")
    updated_by_user = relationship("User", foreign_keys=[updated_by], backref="updated_mappings")

    orgist = relationship("Orgist", foreign_keys=[orgist_id], backref="user_mappings")
    



