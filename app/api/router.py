
from fastapi import APIRouter, HTTPException
from schemas.schemas import PeticionSerieTemporal, PeticionDispersion
from graficadores import serie_temporal, dispersion

router = APIRouter(prefix="/api/v1/graficos", tags=["Graficadores Modulares"])

@router.post("/serie_temporal")
def ep_serie_temporal(peticion: PeticionSerieTemporal):
    print (peticion)
    try:
        ruta = serie_temporal.dibujar(peticion)
        print ("ruta", ruta)

        return {"estado": "exito", "ruta_archivo": ruta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dispersion")
def ep_dispersion(peticion: PeticionDispersion):
    try:
        ruta = dispersion.dibujar(peticion)
        return {"estado": "exito", "ruta_archivo": ruta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))