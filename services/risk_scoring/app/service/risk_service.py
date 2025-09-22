from app.proto import risk_pb2, risk_pb2_grpc

class RiskService(risk_pb2_grpc.RiskServiceServicer):

    def AnalyzeRisk(self, request, context):
        # Arbitrary risk analysis
        is_high_risk = False

        if is_high_risk :
            return risk_pb2.LoanRiskReply(
                decision="REJECTED",
                risk_status="HIGH"
            )
        else:
            return risk_pb2.LoanRiskReply(
                decision="APPROVED",
                risk_status="LOW"
            )