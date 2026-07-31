from enum import Enum
from typing import List, Any, Optional, Literal, Union, Dict
from pydantic import BaseModel, Field, model_validator, ConfigDict

"""
Catalogo de graficas disponibles (Enum) 
#Este es el listado de los graficadores disponibles en la API. 
#Cualquier graficador que se agrega debe agregarse en el listado.
"""
class TipoGraficaEnum(str, Enum):
    serie_temporal = "serie_temporal"
    dispersion = "dispersion"

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
Sub-molde de validacion de cada variable extraida
"""
class DatosVariableSchema (BaseModel):
    valores: Any = Field(..., description="Valores recortados de la variable. Lista simple o anidada")
    unidades_dataset: Optional[str] = Field(..., description="Unidades originales de la variable en el dataset")
    metadata_original: Dict[str, Any] = Field(default_factory=dict, description="Atributos originales de la variable en el NetCDF")
    model_config = ConfigDict(extra="allow")

"""
Sub-molde de validacion de la informacion tecnica
"""
class InfoTecnicaSchema(BaseModel):
    variables: list[str] = Field(..., description="Lista de variables extraidas y disponibles en datos_brutos.")
    lat_real: float = Field(..., description="Latitud exacta del recorte")
    lon_real: float = Field(..., description="Longitud exacta del recorte")
    formas_variables: Dict[str, List[int]] = Field (default_factory=dict, description="Forma de cada variable despues del recorte.")
    model_config = ConfigDict(extra="allow")

"""
Sub-molde de validación del contenido de la llave estetica
"""
class EsteticaSchema(BaseModel):
    nombre_archivo_salida: str
    titulo: str
    xlabel: str
    ylabel: str
    leyenda: bool
    tipo_marca_agua: Optional[TipoMarcaAgua] = Field(default=None, description="Define si se usa marca de agua en malla o en una posición localizada.")
    model_config = ConfigDict(extra="allow")


"""
Sub-molde de validacion de la información que necesita el graficador
"""
class ConfigUsuarioSchema(BaseModel):
    tipo_grafica: TipoGraficaEnum = Field(..., description="Determina el script de enrutamiento")
    variable : Union[str, list[str]] = Field(..., description="Variable o lista de variables a graficar")
    operaciones: List[str] = Field(default_factory=list, description="Operaciones matemáticas solicitadas")
    unidades_esperadas: Optional[Union[str, List[str]]] = Field(default=None, description="Unidades que el usuario espera ver")
    estetica: EsteticaSchema = Field(..., description="Configuración visual heredada")
    model_config = ConfigDict(extra="allow")

"""
Molde Principal: Mensajero universal
"""
class MensajeroExtractorSchema(BaseModel):
    estado: str = Field(..., description="Estado de la extracción (ej. success)")
    datos_brutos: Dict[str, DatosVariableSchema] = Field(..., description="Matriz o lista de datos numéricos recortados")
    fechas: List[str] = Field(default_factory=list, description="Lista de tiempos formateados como strings")
    info_tecnica: InfoTecnicaSchema = Field(..., description="Información recnica del recorte realizado por el extractor")
    config_usuario: ConfigUsuarioSchema = Field(..., description="Configuración usada por el orquestador para enrutar la solicitud")

    @model_validator(mode="after")
    def validar_consistencia_mensajero(self):
        """
        Valida que las variables declaradas en info_tecnica existan en datos_brutos.
        Esta es una validacion universal, util para cualquier tipo de grafica.
        """

        variables_info = set(self.info_tecnica.variables)
        variables_datos = set(self.datos_brutos.keys())

        variables_faltantes = variables_info - variables_datos

        if variables_faltantes:
            raise ValueError(
                f"Las siguientes variables estan declaradas en info_tecnica "
                f"pero no existen en datos_brutos: {list(variables_faltantes)}"
            )

        return self

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow"
    )