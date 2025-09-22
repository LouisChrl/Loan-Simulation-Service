import os
import strawberry
from .gqlTypes import Loan, Check, LoanRequestInput, CheckDepositInput, LoanRequestResponse, CheckDepositResponse
from .httpHelpers import post_json, get_json

# LOAN_BASE = "http://loan_orchestrator:" + os.getenv("CONTAINER_REST_PORT")
CHECK_BASE = "http://bank_check_validation:" + os.getenv("CONTAINER_REST_PORT")

# GraphQL Query (READ)
@strawberry.type
class Query:
    # @strawberry.field
    # async def getLoanInformation(self, loan_id:strawberry.ID) -> Loan:
    #     response = await get_json(LOAN_BASE,f"/loans/{loan_id}")
    #     return Loan(
    #         id = response.get("id"),
    #         loan_amount = response.get("loan_amount"),
    #         loan_status = response.get("loan_status")
    #     )
    
    @strawberry.field
    async def getCheckInformation(self, check_number:str) -> Check:
        response = await get_json(CHECK_BASE,f"/checks/{check_number}")
        return Check(
            id = response.get("id"),
            check_number = response.get("check_number"),
            account_number = response.get("account_number"),
            check_amount = response.get("check_amount"),
            check_status = response.get("check_status")
        )

# GraphQL Mutation (WRITE)
@strawberry.type
class Mutation:
    # @strawberry.mutation
    # async def requestLoan(self, input:LoanRequestInput) -> LoanRequestResponse:
    #     payload = {
    #         "account_number": str(input.account_number),
    #         "loan_amount": input.loan_amount,
    #         "description": input.description
    #     }
    #     response = await post_json(LOAN_BASE, "/loans", payload)
    #     loan = None
    #     if response.get("loan"):
    #         loan = Loan(response.get("loan"))
    #     return LoanRequestResponse(
    #         success = bool(response.get("success")),
    #         message = str(response.get("message")),
    #         loan = loan
    #     )
    
    @strawberry.mutation
    async def depositCheck(self, input:CheckDepositInput) -> CheckDepositResponse:
        payload = {
            "account_number": str(input.account_number),
            "check_number": str(input.check_number),
            "check_account_number": str(input.check_account_number),
            "check_amount": float(input.check_amount)
        }
        response = await post_json(CHECK_BASE, "/checks/deposit", payload)
        return CheckDepositResponse(
            success = bool(response.get("success")),
            message = bool(response.get("message"))
        )
