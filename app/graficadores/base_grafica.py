import os
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from schemas.schemas import MensajeroExtractorSchema, EsteticaSchema
from utils.estilo import aplicar_estilo, marca_agua_localizada, marca_agua_malla

class BaseGrafico(ABC):
    def __init__(self, estilo: EsteticaSchema):
        # Se recibe y se guarda el esquema estetico validado
        self.estilo = estilo 
        self.props_tipograficas = aplicar_estilo(grid=True)

    @abstractmethod
    def plot(self, ax, mensajero: MensajeroExtractorSchema) -> None:
        """
        Cada grafica define su logica aqui. Obliga a cualquier clase que herede 
        esta plantilla a escribir su propioa logica para plotear los datos
        """
        pass

    def configurar_ejes(self, ax) -> None:
        """
        Método concreto: Aplica la identidad institucional del centro.
        Como los títulos, labels y leyendas son comunes, lo resolvemos aquí
        para que ningún graficador tenga que repetir este código.
        """
        ax.set_title(self.estilo.titulo, fontproperties=self.props_tipograficas["titulo"], pad=15)
        ax.set_xlabel(self.estilo.xlabel, fontproperties=self.props_tipograficas["etiquetas"])
        ax.set_ylabel(self.estilo.ylabel, fontproperties=self.props_tipograficas["etiquetas"]) # <-- Corregido set_ylabel

        if self.estilo.leyenda:
            ax.legend(loc='best', prop=self.props_tipograficas["leyenda"])

    def _aplicar_marca_agua(self, fig) -> None:
        """
        Se delega el trabajo de logos a las funciones especializadas en estilo.py
        """
        opcion_marca = self.estilo.tipo_marca_agua
        
        if opcion_marca is None:
            return  
            
        if opcion_marca == "malla":
            # Llamamos a tu función de malla
            marca_agua_malla(fig)
                     
        else:
            # Llamamos a tu función localizada pasándole exactamente el Literal validado
            # (ej: "inf_derecha", "sup_izquierda") que encaja perfecto con tu parámetro "esquina"
            marca_agua_localizada(fig, esquina=opcion_marca)

    def render(self, mensajero: MensajeroExtractorSchema) -> str:
        """
        El 'Template Method' controla el flujo exacto de dibujo.
        Garantiza que todas las salidas de la API sean idénticas en estructura de acuerdo a la identidad DIMAR.
        """
        fig, ax = plt.subplots(figsize=plt.rcParams.get('figure.figsize'))
        
        self.plot(ax, mensajero)

        self.configurar_ejes(ax)

        fig.tight_layout()
        
        self._aplicar_marca_agua(fig)
        
        os.makedirs("salidas", exist_ok=True)
        ruta_salida = f"salidas/{self.estilo.nombre_archivo_salida}"
        
        # savefig.bbox y savefig.dpi ya están manejados por tus rcParams
        fig.savefig(ruta_salida)
        plt.close(fig)

        return ruta_salida












