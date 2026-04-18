from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from utils.renderer import render
app = FastAPI()

@app.get("/test_render", response_class=HTMLResponse)
@render("index.html")
def read_root(request: Request):
   return {
        "titulo": "Prueba de Renderer",
        "usuario": "Programador Pro",
        "items": ["uv", "FastAPI", "Jinja2", "Decoradores"],
        "status": "¡Funciona perfectamente!"
    }