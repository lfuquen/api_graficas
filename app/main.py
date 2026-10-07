import sys
from os import path
from fastapi import FastAPI

sys.path.append(path.dirname(__file__))

from core.config import settings
from api.router import router as graficos_router
from schemas.schemas import PeticionSerieTemporal, PeticionDispersion


app = FastAPI(
    title="API de Graficación SOMO",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"Mi API de graficas": "running!"}


app.include_router(graficos_router)

"""
Endpoints de graficadores
"""
