import os
import uvicorn
from fastapi import FastAPI
from routes.routes import router as checks_router

PORT = int(os.getenv("PORT"))

app = FastAPI(title="bank_check_validation_rest")
app.include_router(checks_router)

@app.get("/healthz")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
