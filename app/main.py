import sys
from os import path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

sys.path.append(path.dirname(__file__))

from core.config import settings
from schemas.schemas import MensajeroExtractorSchema

"""
Importacion de los modulos de graficacion especificos según el tipo de grafica
"""
from graficadores import serie_temporal
from graficadores import dispersion


app = FastAPI(
    title="API de Graficación SOMO",
    version="1.0.0"
)

"""
Este es el MAPA DE ENRUTAMIENTO
Aquí se asociamos exactamente el valor de tu Enum con su archivo físico.
FastAPI sabrá a quien llamar según el tipo de grafica que tenga el mensajero de solicitud 
"""
GRAFICADORES_MAP = {
    "serie_temporal": serie_temporal.dibujar,
    "dispersion": dispersion.dibujar
}


@app.get("/")
def read_root():
    return {"Mi API de graficas": "running!"}


"""
Endpoint principal de graficación
"""
@app.post("/generar-grafica", response_class=JSONResponse)
async def generar_grafica_endpoint(mensajero: MensajeroExtractorSchema):
    """
    Recibe el paquete estandarizado del extractor de Linux, valida las llaves 
    mediante Pydantic y enruta al módulo correspondiente.
    """
    try:
        # Extraer la instrucción validada
        tipo = mensajero.config_usuario.tipo_grafica.value
        
        # Buscar el graficador en el catálogo
        funcion_graficadora = GRAFICADORES_MAP.get(tipo)
        
        if not funcion_graficadora:
            raise HTTPException(
                status_code=501, 
                detail=f"El graficador '{tipo}' no está implementado."
            )
        
        # Delegar el dibujo al módulo especialista (este usa la base_grafica)
        ruta_archivo = funcion_graficadora(mensajero)
        
        return {
            "status": "success",
            "mensaje": "Grafica generada correctamente",
            "ruta_archivo": ruta_archivo
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en la renderización: {str(e)}"
        )

