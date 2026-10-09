
import logging
from fastapi import APIRouter, HTTPException
from schemas.schemas import PeticionSerieTemporal, PeticionDispersion, PeticionBarras, PeticionRosaVientos
from graficadores import serie_temporal, dispersion, barras, rosa_vientos

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/graficos", tags=["Graficadores Modulares"])

@router.post("/serie_temporal")
def ep_serie_temporal(peticion: PeticionSerieTemporal):
    print (peticion)
    try:
        ruta = serie_temporal.dibujar(peticion)
        print ("ruta", ruta)

        return {"estado": "exito", "ruta_archivo": ruta}
    except Exception as e:
        logger.exception("Fallo al generar serie_temporal")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dispersion")
def ep_dispersion(peticion: PeticionDispersion):
    print (peticion)
    try:
        ruta = dispersion.dibujar(peticion)
        return {"estado": "exito", "ruta_archivo": ruta}
    except Exception as e:
        logger.exception("Fallo al generar dispersion")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/barras")
def ep_barras(peticion: PeticionBarras):
    try:
        ruta = barras.dibujar(peticion)
        return {"estado": "exito", "ruta_archivo": ruta}
    except Exception as e:
        logger.exception("Fallo al generar barras")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rosa_vientos")
def ep_rosa_vientos(peticion: PeticionRosaVientos):
    try:
        ruta = rosa_vientos.dibujar(peticion)
        return {"estado": "exito", "ruta_archivo": ruta}
    except Exception as e:
        logger.exception("Fallo al generar rosa_vientos")
        raise HTTPException(status_code=500, detail=str(e))
