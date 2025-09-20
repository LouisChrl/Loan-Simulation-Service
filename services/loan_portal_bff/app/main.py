import os
import uvicorn
import strawberry
from fastapi import FastAPI
from strawberry.schema.config import StrawberryConfig
from strawberry.fastapi import GraphQLRouter
from graph.schema import Query, Mutation

PORT = int(os.getenv("PORT"))

# GraphQL Route and Schema
schema = strawberry.Schema(query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=False))
graphql_app = GraphQLRouter(schema)

# FastAPI app initialization
app = FastAPI(title="loan_portal_bff")
app.include_router(graphql_app, prefix="/graphql")

# Healthchecks
@app.get("/healthz")
def health() -> dict:
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)