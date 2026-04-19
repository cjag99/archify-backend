from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.renderer import render

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/test_render", response_class=HTMLResponse)
@render("index.html")
def read_root(request: Request):
   return {
        "titulo": "Prueba de Renderer",
        "usuario": "Programador Pro",
        "items": ["uv", "FastAPI", "Jinja2", "Decoradores"],
        "status": "¡Funciona perfectamente!"
    }