import sys
from os import path
from contextlib import asynccontextmanager
import matplotlib
from fastapi import FastAPI

# Backend sin pantalla; debe fijarse antes de importar los graficadores (pyplot)
matplotlib.use("Agg")

sys.path.append(path.dirname(__file__))

from core.config import settings
from api.router import router as graficos_router
from schemas.schemas import PeticionSerieTemporal, PeticionDispersion
from utils.estilo.estilo_mapa_color import precargar_capas


@asynccontextmanager
async def lifespan(app: FastAPI):
    precargar_capas()
    yield


app = FastAPI(
    title="API de Graficación SOMO",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"Mi API de graficas": "running!"}


app.include_router(graficos_router)

"""
Endpoints de graficadores
"""
