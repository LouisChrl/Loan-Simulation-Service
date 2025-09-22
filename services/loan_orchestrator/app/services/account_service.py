import re
from sqlalchemy.orm import Session
from orm.orm import Account, Bank

def verifyAccountExistence(db: Session, account_number: str) -> bool:
    return db.query(Account).filter(Account.account_number == account_number).first() is not None

def verifyAccountBalance(db: Session, account_number: str, check_amount: float) -> bool:
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    return bool(acc and acc.balance >= check_amount)

def verifyBankPatternForAccount(db: Session, account_number: str) -> bool:
    # Validate Account Number VS Bank Pattern
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    if not acc:
        return False
    bank = db.query(Bank).filter(Bank.id == acc.bank_id).first()
    return re.fullmatch(bank.account_number_validity_pattern, account_number) is not None
