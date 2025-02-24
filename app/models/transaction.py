from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    amount = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False)
    pan = Column(String(255), nullable=False)  # Encrypted PAN
    processing_code = Column(String(6), nullable=False)
    merchant_id = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default='pending')
    status_updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    billing_code_id = Column(Integer, ForeignKey("billing_codes.id"))

    billing_code = relationship("BillingCode", back_populates="transactions")
