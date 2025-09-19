import strawberry
from typing import Optional

@strawberry.type
class Loan:
    id: strawberry.ID
    account_number: str
    loan_amount: float
    status: str

@strawberry.type
class Check:
    id: strawberry.ID
    check_number: str
    bank_id: str
    account_number: str
    check_amount: float
    status: str

@strawberry.input
class LoanRequestInput:
    account_number: str
    loan_amount: float
    description: Optional[str] = None

@strawberry.input
class CheckDepositInput:
    account_number: str
    check_number: str
    check_bank_id: str
    check_account_number: str
    check_amount: float

@strawberry.type
class LoanRequestResponse:
    success: bool
    message: str
    loan: Optional[Loan] = None

@strawberry.type
class CheckDepositResponse:
    success: bool
    message: str