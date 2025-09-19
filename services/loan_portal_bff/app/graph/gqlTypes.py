import strawberry
from typing import Optional

@strawberry.type
class Loan:
    id: strawberry.ID
    account_number: str
    loan_amount: float
    loan_status: str

@strawberry.type
class Check:
    id: strawberry.ID
    check_number: str
    account_number: str
    check_amount: float
    check_status: str

@strawberry.input
class LoanRequestInput:
    account_number: str
    loan_amount: float
    description: Optional[str] = None

@strawberry.input
class CheckDepositInput:
    account_number: str
    check_number: str
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