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
    #         id = response["id"],
    #         loan_amount = response["loan_amount"],
    #         loan_status = response["status"]
    #     )
    
    @strawberry.field
    async def getCheckInformation(self, check_id:strawberry.ID) -> Check:
        response = await get_json(CHECK_BASE,f"/checks/{check_id}")
        return Check(
            id = response["id"],
            check_number = response["check_number"],
            account_number = response["account_number"],
            check_amount = response["check_amount"],
            check_status = response["status"]
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
    #         loan = Loan(
    #             id = response["loan"]["id"],
    #             account_number = response["loan"]["account_number"],
    #             loan_amount = response["loan"]["loan_amount"],
    #             loan_status = response["loan"]["loan_status"]
    #         )
    #     return LoanRequestResponse(
    #         success = bool(response["success"]),
    #         message = str(response["message"]),
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
        response = post_json(CHECK_BASE, "/checks/deposit", payload)
        return CheckDepositResponse(
            success = response["success"],
            message = response["message"]
        )
