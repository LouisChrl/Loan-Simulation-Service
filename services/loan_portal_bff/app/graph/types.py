import strawberry
from typing import Optional

@strawberry.type
class Loan:
    id: strawberry.ID
    status: str
    loanAmount: float
    loanType: str
    riskLevel: Optional[str] = None
