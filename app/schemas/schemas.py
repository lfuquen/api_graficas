
from typing import Annotated, List, Optional, Literal, Union, Dict
from pydantic import BaseModel, ConfigDict, Field, model_validator

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
Sub-esquema exclusivo para Barras.
"""
class EsteticaBarrasSchema(EsteticaSchema):
    xlabel: Optional[str] = ""  # Heredado de EsteticaSchema; explicito por claridad del contrato
    tipo_marca_agua: Optional[TipoMarcaAgua] = Field(default="centro")  # Heredado; explicito por claridad del contrato
    ancho_barra: Optional[float] = Field(default=None, gt=0, le=1)
    color_borde: Optional[str] = None
    grosor_borde: Optional[float] = Field(default=None, ge=0)
    alpha: Optional[float] = Field(default=None, ge=0, le=1)
    mostrar_valores: Optional[bool] = None
    formato_valores: Optional[str] = None
    tamano_valores: Optional[int] = Field(default=None, gt=0)
    rotacion_etiquetas: Optional[int] = None
    rejilla_eje_valores: Optional[bool] = None

"""
DTOs de Petición por Endpoint
"""
class PeticionSerieTemporal(BaseModel):
    fechas: List[str]
    datos: Dict[str, List[float]]
    estetica: EsteticaSchema

    @model_validator(mode="after")
    def validar_longitudes(self):
        if not self.datos:
            raise ValueError("'datos' debe contener al menos una serie")
        n = len(self.fechas)
        for nombre, valores in self.datos.items():
            if len(valores) != n:
                raise ValueError(
                    f"La serie '{nombre}' tiene {len(valores)} valores; se esperaban {n} (uno por fecha)"
                )
        return self

class PeticionDispersion(BaseModel):
    variable_x: VariableScatter
    variable_y: VariableScatter
    estetica: EsteticaSchema

    @model_validator(mode="after")
    def validar_longitudes(self):
        nx, ny = len(self.variable_x.valores), len(self.variable_y.valores)
        if nx != ny:
            raise ValueError(
                f"'{self.variable_x.nombre}' tiene {nx} valores y '{self.variable_y.nombre}' tiene {ny}; deben coincidir"
            )
        return self

class PeticionBarras(BaseModel):
    categorias: List[str]
    datos: Dict[str, List[float]]
    orientacion: Literal["vertical", "horizontal"] = "vertical"
    apiladas: bool = False
    estetica: EsteticaBarrasSchema

    @model_validator(mode="after")
    def validar_longitudes(self):
        if not self.datos:
            raise ValueError("'datos' debe contener al menos una serie")
        n = len(self.categorias)
        for nombre, valores in self.datos.items():
            if len(valores) != n:
                raise ValueError(
                    f"La serie '{nombre}' tiene {len(valores)} valores; se esperaban {n} (uno por categoria)"
                )
        return self

class PeticionRosaVientos(BaseModel):
    direcciones: List[Annotated[float, Field(ge=0, le=360)]]
    velocidades: List[Annotated[float, Field(ge=0)]]
    unidades: str = "m/s"
    n_sectores: Literal[8, 16, 32] = 16
    intervalos_velocidad: Optional[List[Annotated[float, Field(ge=0)]]] = None   # None = calculo segun los datos
    umbral_calma: float = Field(default=0.5, ge=0)
    estetica: EsteticaSchema

    @model_validator(mode="after")
    def validar_datos(self):
        if not self.direcciones:
            raise ValueError("'direcciones' debe contener al menos un valor")
        if len(self.direcciones) != len(self.velocidades):
            raise ValueError(
                f"'direcciones' tiene {len(self.direcciones)} valores y 'velocidades' tiene {len(self.velocidades)}; deben coincidir"
            )
        if self.intervalos_velocidad is not None:
            if not self.intervalos_velocidad:
                raise ValueError("'intervalos_velocidad' no puede ser una lista vacia")
            if any(b <= a for a, b in zip(self.intervalos_velocidad, self.intervalos_velocidad[1:])):
                raise ValueError("'intervalos_velocidad' debe ser estrictamente creciente")
        return self