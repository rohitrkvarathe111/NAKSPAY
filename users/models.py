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

    user_mappings = relationship("UserMapping", foreign_keys="[UserMapping.user_id]", back_populates="user")
    mapped_mappings = relationship("UserMapping", foreign_keys="[UserMapping.mapped_user_id]", back_populates="mapped_user")
    requested_user = relationship("UserMapping", foreign_keys="[UserMapping.requested_user_id]", back_populates="requested_user")
    created_mappings = relationship("UserMapping", foreign_keys="[UserMapping.created_by]", back_populates="created_by_user")
    updated_mappings = relationship("UserMapping", foreign_keys="[UserMapping.updated_by]", back_populates="updated_by_user")





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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mapped_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mapped_orgist_id = Column(Integer, ForeignKey("orgist.id"), nullable=True)
    requested_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mapped_status = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="user_mappings")
    mapped_user = relationship("User", foreign_keys=[mapped_user_id], back_populates="mapped_mappings")
    requested_user = relationship("User", foreign_keys=[requested_user_id], back_populates="requested_user")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="created_mappings")
    updated_by_user = relationship("User", foreign_keys=[updated_by], back_populates="updated_mappings")

    # for orgist side — you can still use back_populates if Orgist has relationships
    orgist = relationship("Orgist", foreign_keys=[orgist_id], back_populates="user_mappings")
    mapped_orgist = relationship("Orgist", foreign_keys=[mapped_orgist_id], back_populates="mapped_mappings")



