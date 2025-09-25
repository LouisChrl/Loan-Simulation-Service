import re
from decimal import Decimal
from sqlalchemy.orm import Session
from orm.orm import Account, Bank

def verifyAccountExistence(db: Session, account_number: str) -> bool:
    return db.query(Account).filter(Account.account_number == account_number).first() is not None

def verifyBankPatternForAccount(db: Session, account_number: str) -> bool:
    # Validate Account Number VS Bank Pattern
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    if not acc:
        return False
    bank = db.query(Bank).filter(Bank.id == acc.bank_id).first()
    return re.fullmatch(bank.account_number_validity_pattern, account_number) is not None

def getBalance(db: Session, account_number: str) -> float:
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    return acc.balance

def addBalance(db: Session, account_number: str, amount: float) -> float:
    if amount <= 0:
        raise ValueError("amount must be > 0")
    
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    acc.balance += amount
    db.flush()
    db.refresh(acc)
    return acc.balance