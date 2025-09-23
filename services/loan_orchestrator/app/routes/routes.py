from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, condecimal
from sqlalchemy.orm import Session
from db.database import get_db
from orm.orm import Loan
from services.account_service import verifyAccountExistence, verifyAccountBalance, verifyBankPatternForAccount
from services.bank_service import verifyBankExistence
from services.loan_service import create_pending_loan, get_risk_status, get_loan_status, update_loan_status # request_funds

router = APIRouter(prefix="/loans", tags=["loans"])

# --------------------- Schemas (Pydantic) ---------------------

class LoanDTO(BaseModel):
    id: int
    account_number: str
    loan_amount: condecimal(max_digits=12, decimal_places=2)
    loan_status: str

    class Config:
        from_attributes = True  # Pydantic v2

class RequestLoanPayload(BaseModel):
    account_number: str
    loan_amount: condecimal(max_digits=12, decimal_places=2)

class RequestLoanResponse(BaseModel):
    success: bool
    message: str
    loan: Optional[LoanDTO] = None

# ----------------------- Endpoints ----------------------------

@router.get("/{loan_id}", response_model=LoanDTO)
def getLoanInformation(loan_id: int, db: Session = Depends(get_db)):
    loan: Loan | None = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return LoanDTO.model_validate(loan)


@router.post("/request", response_model=RequestLoanResponse)
def requestLoan(payload: RequestLoanPayload, db: Session = Depends(get_db)):
    # 0) Existence of the account, existence of the bank, account number validation
    if not verifyAccountExistence(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Account not found")

    if not verifyBankExistence(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Bank not found for the given account")

    if not verifyBankPatternForAccount(db, payload.account_number):
        raise HTTPException(status_code=400, detail="Account number does not match the bank pattern")

    # 1) Create a loan instance
    loan = create_pending_loan(db, payload.account_number, payload.loan_amount)

    # 2) Risk Scoring
    risk_status, decision = get_risk_status(loan_id=loan.id, account_number=payload.account_number)

    if decision == "REJECT":
        loan = update_loan_status(db, loan.id, "REJECTED")
        return RequestLoanResponse(
            success=False,
            message=f"Rejected by risk scoring (risk_status={risk_status})",
            loan=LoanDTO.model_validate(loan)
        )

    if decision == "REVIEW":
        loan = update_loan_status(db, loan.id, "REVIEW")
        return RequestLoanResponse(
            success=False,
            message=f"Manual review required (risk_status={risk_status})",
            loan=LoanDTO.model_validate(loan)
        )

    # 4) Provider funding
    # ok, provider_msg = request_funds(
    #     account_number=payload.account_number,
    #     amount=float(payload.loan_amount)
    # )

    # if not ok:
    #     loan = update_loan_status(db, loan.id, "FAILED_FUNDING")
    #     return RequestLoanResponse(
    #         success=False,
    #         message=f"Funding rejected: {provider_msg}",
    #         loan=LoanDTO.model_validate(loan)
    #     )

    # 5) Succès → APPROVED
    loan = update_loan_status(db, loan.id, "APPROVED")
    return RequestLoanResponse(
        success = True,
        message = f"Loan approved and funded (risk_status={risk_status})",
        loan = LoanDTO(
            id = loan.id,
            account_number = loan.account_number,
            loan_amount = loan.loan_amount,
            loan_status = loan.loan_status
        )
    )
