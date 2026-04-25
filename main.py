import os
import logging
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.renderer import render
from supabase import Client

load_dotenv()

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
db_params = {
    "url": os.getenv("SUPABASE_URL"),
    "key": os.getenv("SUPABASE_KEY")
}

logging.info(f"Supabase URL: {db_params['url']}")
logging.info(f"Supabase Key: {db_params['key']}")
if db_params.get("url") and db_params.get("key"):
    supabase = Client(db_params["url"], db_params["key"])

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