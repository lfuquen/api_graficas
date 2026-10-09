import pandas as pd
import matplotlib.pyplot as plt
import itertools
from graficadores.base_grafica import BaseGrafico
from schemas.schemas import PeticionSerieTemporal

class SerieTemporalGrafico(BaseGrafico):

    # Ajustes esteticos propios de serie temporal (configuracion sencilla, sin archivo exclusivo en utils/estilo)
    GROSOR_LINEA = 1.5
    ROTACION_FECHAS = 0

    def plot(self, ax: plt.Axes, peticion: PeticionSerieTemporal) -> None:
        """
        Bloque de Dibujo: Implementa el BaseGrafico.
        """

        fechas_dt = pd.to_datetime(peticion.fechas)
       
        colores_disponibles = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ciclo_colores = itertools.cycle(colores_disponibles)
            
        for nombre_variable, valores in peticion.datos.items():
            
            ax.plot(
                fechas_dt, 
                valores, 
                label=nombre_variable,
                linewidth=self.GROSOR_LINEA,
                color=next(ciclo_colores)
            )

        ax.tick_params(axis='x', rotation=self.ROTACION_FECHAS)

def dibujar(peticion: PeticionSerieTemporal) -> str:
    """
   Enrutamiento a api/router.py
    """

    graficador = SerieTemporalGrafico(estilo=peticion.estetica)    
    return graficador.render(peticion)