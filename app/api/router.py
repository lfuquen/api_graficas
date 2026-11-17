
import logging
from threading import Lock
from fastapi import APIRouter, HTTPException, Response
from schemas.schemas import PeticionSerieTemporal, PeticionDispersion, PeticionBarras, PeticionRosaVientos, PeticionMapaColor
from graficadores import serie_temporal, dispersion, barras, rosa_vientos, mapa_color

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/graficos", tags=["Graficadores Modulares"])

# pyplot y rcParams son globales: una grafica a la vez por proceso (aplicar_estilo corre en el constructor)
LOCK_GRAFICOS = Lock()
RESPUESTA_PNG = {200: {"content": {"image/png": {}}}}


def _responder_png(graficador, peticion, nombre: str) -> Response:
    try:
        with LOCK_GRAFICOS:
            png = graficador.dibujar(peticion)
    except Exception:
        logger.exception("Fallo al generar %s", nombre)
        raise HTTPException(status_code=500, detail=f"No se pudo generar la grafica {nombre}")
    return Response(
        content=png,
        media_type="image/png",
        headers={"Content-Disposition": f'inline; filename="{nombre}.png"'},
    )


@router.post("/serie_temporal", response_class=Response, responses=RESPUESTA_PNG)
def ep_serie_temporal(peticion: PeticionSerieTemporal):
    return _responder_png(serie_temporal, peticion, "serie_temporal")

@router.post("/dispersion", response_class=Response, responses=RESPUESTA_PNG)
def ep_dispersion(peticion: PeticionDispersion):
    return _responder_png(dispersion, peticion, "dispersion")

@router.post("/barras", response_class=Response, responses=RESPUESTA_PNG)
def ep_barras(peticion: PeticionBarras):
    return _responder_png(barras, peticion, "barras")

@router.post("/rosa_vientos", response_class=Response, responses=RESPUESTA_PNG)
def ep_rosa_vientos(peticion: PeticionRosaVientos):
    return _responder_png(rosa_vientos, peticion, "rosa_vientos")

@router.post("/mapa_color", response_class=Response, responses=RESPUESTA_PNG)
def ep_mapa_color(peticion: PeticionMapaColor):
    return _responder_png(mapa_color, peticion, "mapa_color")
