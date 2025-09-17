import os
import uvicorn
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graph.schema import Query

CONTAINER_BFF_PORT = int(os.getenv("CONTAINER_BFF_PORT"))

# GraphQL Route and Schema
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# FastAPI app initialization
app = FastAPI(title="loan_portal_bff")
app.include_router(graphql_app, prefix="/graphql")

@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=CONTAINER_BFF_PORT)