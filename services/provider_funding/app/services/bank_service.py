import re
from sqlalchemy.orm import Session
from orm.orm import Account, Bank

def verifyBankExistence(db: Session, account_number: str) -> bool:
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    bank = db.query(Bank).filter(Bank.id == acc.bank_id).first()
    if not bank:
        return False
    else :
        return True
