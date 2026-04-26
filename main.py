from fastapi import FastAPI
from app.api.endpoints import auth

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Welcome to the Auth API!"}