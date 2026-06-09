"""
AMKA — Data Models
SQLAlchemy ORM models for Users, Transactions, Insights, and CreditReports.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    AMKA User model.
    Represents a user of the AMKA financial assistant.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    language = Column(String(10), default='en', nullable=False)  # en, zu, xh, sw, ha
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    transactions = relationship('Transaction', back_populates='user', cascade='all, delete-orphan')
    insights = relationship('Insight', back_populates='user', cascade='all, delete-orphan')
    credit_reports = relationship('CreditReport', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User {self.phone_number} ({self.language})>"


class Transaction(Base):
    """
    AMKA Transaction model.
    Represents a single income or expense transaction.
    """
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    type = Column(String(10), nullable=False)  # 'income' or 'expense'
    amount = Column(Float, nullable=False)
    category = Column(String(50), default='other', nullable=False)  # stock, transport, food, equipment, rent, other
    raw_message = Column(Text, nullable=True)  # Original user message for debugging
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship('User', back_populates='transactions')
    
    def __repr__(self):
        return f"<Transaction {self.type} R{self.amount} ({self.category})>"


class Insight(Base):
    """
    AMKA Insight model.
    Represents an AI-generated business insight sent to a user.
    """
    __tablename__ = 'insights'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    type = Column(String(30), nullable=False)  # weekly_summary, pattern_alert, anomaly, etc.
    content = Column(Text, nullable=False)  # The insight message
    delivered = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='insights')
    
    def __repr__(self):
        return f"<Insight {self.type} ({'delivered' if self.delivered else 'pending'})>"


class CreditReport(Base):
    """
    AMKA CreditReport model.
    Represents a generated financial behaviour report for credit applications.
    """
    __tablename__ = 'credit_reports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    total_income = Column(Float, default=0.0, nullable=False)
    total_expenses = Column(Float, default=0.0, nullable=False)
    net_profit = Column(Float, default=0.0, nullable=False)
    active_days = Column(Integer, default=0, nullable=False)
    consistency_score = Column(Integer, default=0, nullable=False)  # 0-100
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='credit_reports')
    
    def __repr__(self):
        return f"<CreditReport R{self.net_profit} (Score: {self.consistency_score})>"