from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import admin, auth, projects, patterns



app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(patterns.router, prefix="/patterns", tags=["patterns"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Welcome to the Auth API!"}