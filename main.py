"""
Main module for the Archify FastAPI backend application.

This module initializes the FastAPI application, configures CORS middleware,
and includes routers for various API endpoints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.endpoints import auth, projects, patterns, architectures, users, code_language, patterns_code, images
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://archify-frontend.vercel.app/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(patterns.router, prefix="/patterns", tags=["patterns"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(architectures.router, prefix="/architectures", tags=["architectures"])
app.include_router(code_language.router, prefix="/code-languages", tags=["code-languages"])
app.include_router(patterns_code.router, prefix="/patterns-code", tags=["patterns-code"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs", status_code=301)