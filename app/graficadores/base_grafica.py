import os
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from schemas.schemas import EsteticaSchema
from utils.estilo import aplicar_estilo, roles_tipograficos, aplicar_marca_agua, marca_agua_localizada, marca_agua_malla

class BaseGrafico(ABC):
    def __init__(self, estilo: EsteticaSchema):
        self.estilo = estilo 
        self.props_tipograficas = aplicar_estilo(grid=True)

    @abstractmethod
    def plot(self, ax: plt.Axes, peticion) -> None:
        """ 
        Metodo abstracto que implementacion cada grafocador especializado
        """
        pass

    def configurar_ejes(self, ax: plt.Axes) -> None:
        """
        Método concreto: Aplica las tipografías asignadas por rol (titulo, etiquetas, leyenda).
        """
        if self.estilo.titulo:
            ax.set_title(
                self.estilo.titulo,
                fontproperties=self.props_tipograficas["titulo"],
                pad=15
            )
        if self.estilo.xlabel:
            ax.set_xlabel(
                self.estilo.xlabel,
                fontproperties=self.props_tipograficas["etiquetas"]
            )
        if self.estilo.ylabel:
            ax.set_ylabel(
                self.estilo.ylabel,
                fontproperties=self.props_tipograficas["etiquetas"]
            )
        if self.estilo.leyenda:
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                ax.legend(loc="best", prop=self.props_tipograficas["leyenda"])

    def _aplicar_marca_agua(self, fig: plt.Figure) -> None:
        """
        Se delega el trabajo de logos a las funciones especializadas en marca_agua.py
        """
        opcion_marca = self.estilo.tipo_marca_agua
        if opcion_marca is None:
            return  
            
        if "aplicar_marca_agua" in globals():
            aplicar_marca_agua(fig, opcion=opcion_marca)
        else:
            if opcion_marca == "malla":
                marca_agua_malla(fig)
            else:
                marca_agua_localizada(fig, modo=opcion_marca)

    def render(self, peticion) -> str:
        """
        El 'Template Method' controla el flujo exacto de dibujo.
        Garantiza que todas las salidas de la API sean idénticas en estructura de acuerdo a la identidad DIMAR.
        """
        fig, ax = plt.subplots()
        
        self.plot(ax, peticion)

        self.configurar_ejes(ax)

        fig.tight_layout()
        
        self._aplicar_marca_agua(fig)
        
        os.makedirs("salidas", exist_ok=True)
        ruta_salida = f"salidas/{self.estilo.nombre_archivo_salida}"
        fig.savefig(ruta_salida)
        plt.close(fig)

        return ruta_salida