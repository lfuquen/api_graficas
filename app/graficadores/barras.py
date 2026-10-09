import itertools
import numpy as np
import matplotlib.pyplot as plt
from graficadores.base_grafica import BaseGrafico
from schemas.schemas import PeticionBarras, EsteticaBarrasSchema
from utils.estilo import EstiloBarras, kwargs_barra, anotar_valores, configurar_rejilla, configurar_categorias


class BarrasGrafico(BaseGrafico):

    def __init__(self, estilo: EsteticaBarrasSchema):
        super().__init__(estilo)
        self.estilo_barras = EstiloBarras.desde_estetica(estilo)

    def plot(self, ax: plt.Axes, peticion: PeticionBarras) -> None:
        """
        Bloque de Dibujo: Implementa el BaseGrafico.
        Soporta barras agrupadas o apiladas, en orientacion vertical u horizontal.
        La estetica especifica se delega a utils/estilo/estilo_barras.py
        """
        
        estilo = self.estilo_barras
        categorias = peticion.categorias
        series = peticion.datos
        horizontal = peticion.orientacion == "horizontal"

        posiciones = np.arange(len(categorias))
        n_series = len(series)

        colores_disponibles = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ciclo_colores = itertools.cycle(colores_disponibles)

        # Barras apiladas comparten posicion; agrupadas se desplazan dentro del ancho total
        ancho = estilo.ancho_barra if peticion.apiladas else estilo.ancho_barra / n_series
        acumulado = np.zeros(len(categorias))

        for i, (nombre_variable, valores) in enumerate(series.items()):
            valores = np.asarray(valores, dtype=float)

            if peticion.apiladas:
                desplazamiento = posiciones
                base = acumulado.copy()
                acumulado += valores
            else:
                desplazamiento = posiciones + (i - (n_series - 1) / 2) * ancho
                base = None

            comunes = dict(label=nombre_variable, color=next(ciclo_colores), **kwargs_barra(estilo))

            if horizontal:
                barras = ax.barh(desplazamiento, valores, height=ancho, left=base, **comunes)
            else:
                barras = ax.bar(desplazamiento, valores, width=ancho, bottom=base, **comunes)

            anotar_valores(ax, barras, estilo, peticion.apiladas)

        configurar_rejilla(ax, horizontal, estilo)
        configurar_categorias(ax, posiciones, categorias, horizontal, estilo)


def dibujar(peticion: PeticionBarras) -> str:
    """
    Enrutamiento a api/router.py
    """
    graficador = BarrasGrafico(estilo=peticion.estetica)
    return graficador.render(peticion)
