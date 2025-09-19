from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, ForeignKey, Text

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

class Bank(Base):
    __tablename__ = "bank"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    account_number_validity_pattern: Mapped[str] = mapped_column(String(100), nullable=False)
    check_validity_pattern: Mapped[str] = mapped_column(String(100), nullable=False)

class Account(Base):
    __tablename__ = "account"
    account_number: Mapped[str] = mapped_column(String(20), primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)
    bank_id: Mapped[int] = mapped_column(ForeignKey("bank.id"), nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

class Check(Base):
    __tablename__ = "cashier_check"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_number: Mapped[str] = mapped_column(ForeignKey("account.account_number"), nullable=False)
    check_number: Mapped[str] = mapped_column(String(50), nullable=False)
    check_amount: Mapped[float] = mapped_column(Float, nullable=False)
    check_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
