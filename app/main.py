from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Asegurar que el path sea correcto para encontrar el módulo 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import engine
from app.sql_model import Base
from app.routers.main_router import router as main_router
#from app.auth_middleware import auth_middleware
from app.middleware.auth import auth_middleware
from app.middleware.logging import logging_middleware

app = FastAPI()

# Configuración de la App
app.mount("/static", StaticFiles(directory="static"), name="static")
app.middleware("http")(auth_middleware)
app.middleware("http")(logging_middleware)
app.include_router(main_router)

@app.get("/")
def read_root():
    return {"message": "Hola desde FastAI/FastAPI"}

# --- MÉTODO MAIN ---
def main():
    """
    Punto de entrada para la ejecución de la aplicación.
    Aquí puedes añadir configuraciones previas al arranque.
    """
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    # Iniciar servidor
    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True)

if __name__ == "__main__":
    main()