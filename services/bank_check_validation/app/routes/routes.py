from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db.database import get_db, SessionLocal
from orm.orm import BankCheck
from services.account_service import verifyAccountExistence, verifyAccountBalance
from services.bank_service import verifyBankExistence, verifyCheckNumber

router = APIRouter(prefix="/checks", tags=["checks"])

class DepositCheckPayload(BaseModel):
    account_number: str
    check_number: str
    check_account_number: str
    check_amount: float = Field(gt=0)

class CheckResponse(BaseModel):
    id: int
    check_number: str
    account_number: str
    check_amount: float
    check_status: str

@router.post("/deposit")
def deposit_check(payload: DepositCheckPayload, db: Session = Depends(get_db)):
    # 1) Existence of the emitting account
    if not verifyAccountExistence(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Emitter account not found")

    # 2) Existence of the bank
    if not verifyBankExistence(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Bank not found")

    # 3) Check number validation
    if not verifyCheckNumber(db, payload.account_number, payload.check_number):
        raise HTTPException(status_code=400, detail="Invalid check number format")

    # 4) Account balance validation
    if not verifyAccountBalance(db, payload.account_number, payload.check_amount):
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 5) Persistence for validated checks
    check = BankCheck(
        account_number=payload.account_number,
        check_number=payload.check_number,
        check_amount=payload.check_amount,
        check_status="issued"
    )
    db.add(check)
    db.commit()
    db.refresh(check)

    return {"success": True, "message": "The check deposit was successful", "checkId": check.id}

@router.get("/{check_number}", response_model=CheckResponse)
def get_check_information(check_number: str, db: Session = Depends(get_db)):
    c = db.query(BankCheck).filter(BankCheck.check_number == check_number).first()
    if not c:
        raise HTTPException(status_code=404, detail="Check not found")
    return CheckResponse(
        id=c.id,
        check_number=c.check_number,
        account_number=str(c.account_number),
        check_amount=float(c.check_amount),
        check_status=c.check_status
    )
