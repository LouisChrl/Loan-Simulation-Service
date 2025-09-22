# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copying requirements file first to leverage Docker cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# .proto file compilation
RUN python -m grpc_tools.protoc \
    -Iapp/proto \
    --python_out=app/proto \
    --grpc_python_out=app/proto \
    app/proto/risk.proto

RUN sed -i 's/^import risk_pb2/from app.proto import risk_pb2/' app/proto/risk_pb2_grpc.py

CMD ["python", "-m", "app.main"]