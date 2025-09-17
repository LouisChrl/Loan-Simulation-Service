import strawberry
from typing import Optional

# On prépare déjà un type pour la suite (même s'il n'est pas encore utilisé)
@strawberry.type
class Loan:
    id: strawberry.ID
    status: str
    loanAmount: float
    loanType: str
    riskLevel: Optional[str] = None
