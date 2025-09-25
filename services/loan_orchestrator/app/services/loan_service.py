from typing import Literal, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
import httpx
from orm.orm import Loan
import os
import grpc
from proto import risk_pb2, risk_pb2_grpc

RiskDecision = Literal["PENDING", "APPROVED", "REJECTED", "REVIEW", "FUNDED", "CANCELLED"]
RiskStatus = Literal["HIGH", "LOW"]

# ---------------- Core Loan Operations (DB) -----------------
def create_pending_loan(db: Session, account_number: str, amount: Decimal) -> Loan:
    loan = Loan(account_number=account_number, loan_amount=amount, loan_status="PENDING")
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def get_loan_status(db: Session, loan_id: int) -> str | None:
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    return None if not loan else loan.loan_status

def update_loan_status(db: Session, loan_id: int, new_status: str) -> Loan | None:
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        return None
    loan.loan_status = new_status
    db.commit()
    db.refresh(loan)
    return loan

# ---- External Operations : Risk (gRPC) & Funding (REST) ----

def get_risk_status(loan_id: int, account_number: str) -> Tuple[RiskStatus, RiskDecision]:
    target = os.getenv("RISK_GRPC_ADDR")

    # options = [
    #     ("grpc.keepalive_time_ms", 30_000),
    #     ("grpc.http2.max_pings_without_data", 0),
    #     ("grpc.max_receive_message_length", 20 * 1024 * 1024),
    # ]

    try:
        with grpc.insecure_channel(target) as channel:
            stub = risk_pb2_grpc.RiskServiceStub(channel)
            req = risk_pb2.LoanRiskRequest(loan_id=loan_id, account_number=account_number)
            res = stub.AnalyzeRisk(req, timeout=3.0)

        decision_raw = (res.decision or "").upper()
        if decision_raw.startswith("APPROVED") or decision_raw.startswith("APPROVE"):
            decision: RiskDecision = "APPROVED"
        elif decision_raw.startswith("REJECT"):
            decision = "REJECTED"
        else:
            decision = "CANCELLED"

        risk_status = (getattr(res, "risk_status", "") or "").upper()

        return risk_status, decision

    except grpc.RpcError:
        return "UNKNOWN", "REVIEW"

async def request_funds(account_number: str, amount: float) -> Tuple[bool, str]:
    provider_url = os.getenv("PROVIDER_URL")
    payload = {"account_number": account_number, "amount": amount}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(provider_url, json=payload)
        if r.status_code != 200:
            try:
                msg = r.json().get("provider_msg", r.text)
            except Exception:
                msg = r.text
            return False, f"provider funding error: {msg}"
        data = r.json()
        ok = bool(data.get("ok"))
        provider_msg = str(data.get("provider_msg"))
        return ok, provider_msg
    except httpx.RequestError as e:
        return False, f"provider funding unreachable: {e}"
