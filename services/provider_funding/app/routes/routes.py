from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, condecimal
from sqlalchemy.orm import Session
from db.database import get_db
from services.account_service import verifyAccountExistence, verifyBankPatternForAccount, getBalance, addBalance
from services.bank_service import verifyBankExistence

router = APIRouter(prefix="", tags=["fund"])

# --------------------- Schemas (Pydantic) ---------------------

class RequestFundPayload(BaseModel):
    account_number: str
    amount: float

class RequestFundResponse(BaseModel):
    ok: bool
    provider_msg: str

# ----------------------- Endpoints ----------------------------

@router.post("/", response_model=RequestFundResponse)
def requestFunds(payload: RequestFundPayload, db: Session = Depends(get_db)):
    # 0) Existence of the account, existence of the bank, account number validation
    if not verifyAccountExistence(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Account not found")

    if not verifyBankExistence(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Bank not found for the given account")

    if not verifyBankPatternForAccount(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Account number does not match the bank pattern")

    # 1) Add balance to the account
    old_balance = getBalance(db, payload.account_number)
    new_balance = addBalance(db, payload.account_number, payload.amount)
    funded_amount = new_balance - old_balance

    # Commit in database
    db.commit()
    
    # 3) Return message
    ok = True
    provider_msg = f"Account funded : {funded_amount}"
    return RequestFundResponse(
        ok = ok,
        provider_msg = provider_msg
    )
