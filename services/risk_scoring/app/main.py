import grpc
from concurrent import futures
from .service.risk_service import RiskService
from .proto import risk_pb2_grpc
import os

PORT = os.getenv("PORT")

if not PORT:
    raise ValueError("PORT environment variable is not set.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    risk_pb2_grpc.add_RiskServiceServicer_to_server(RiskService(), server)

    server.add_insecure_port(f'[::]:{PORT}')
    print(f"Risk Service gRPC server running on port {PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()