import os
import uvicorn
from fastapi import FastAPI
from routes.routes import router as orchestrator_router

PORT = int(os.getenv("PORT"))

app = FastAPI(title="loan_orchestrator")
app.include_router(orchestrator_router)

@app.get("/healthz")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
