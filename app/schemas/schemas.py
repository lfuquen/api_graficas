
from typing import List, Optional, Literal, Union, Dict
from pydantic import BaseModel, ConfigDict, Field

"""
Opciones de marca de agua localizada 
"""
MarcaAguaLocalizada = Literal[
    "centro",
    "inf_derecha",
    "inf_izquierda",
    "sup_derecha",
    "sup_izquierda"]

"""
Tipos de marca de agua disponibles
"""
TipoMarcaAgua = Union[
    Literal["malla"],
    MarcaAguaLocalizada
]
"""
Desificiones estetica
"""
class EsteticaSchema(BaseModel):
    nombre_archivo_salida: str = "salida.png"
    titulo: Optional[str] = ""
    xlabel: Optional[str] = ""
    ylabel: Optional[str] = ""
    leyenda: bool = True
    tipo_marca_agua: Optional[TipoMarcaAgua] = Field(default="centro")
    model_config = ConfigDict(extra="allow")

"""
Sub-esquema exclusivo para Dispersión
"""
class VariableScatter(BaseModel):
    nombre: str
    valores: List[float]
    unidades: Optional[str] = None

"""
DTOs de Petición por Endpoint
"""
class PeticionSerieTemporal(BaseModel):
    fechas: List[str] 
    datos: Dict[str, List[float]]
    estetica: EsteticaSchema

class PeticionDispersion(BaseModel):
    variable_x: VariableScatter = ""
    variable_y: VariableScatter = ""
    estetica: EsteticaSchema