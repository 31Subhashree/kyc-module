from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class UserKYC(Base):
    __tablename__ = "user_kyc"

    id = Column(Integer, primary_key=True, index=True)
    pan_number = Column(String(10), unique=True, nullable=False)
    account_number = Column(String(20), unique=True, nullable=True)
    ifsc_code = Column(String(11), nullable=True)
    pan_verified = Column(Boolean, default=False)
    bank_verified = Column(Boolean, default=False)
