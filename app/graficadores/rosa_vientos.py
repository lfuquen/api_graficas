import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from graficadores.base_grafica import BaseGrafico
from schemas.schemas import PeticionRosaVientos, EsteticaSchema
from utils.estilo import (
    EstiloRosaVientos,
    colores_por_intervalo,
    etiquetas_intervalos,
    configurar_ejes_polares,
    anotar_pie
)

N_INTERVALOS_AUTO = 5
PERCENTIL_REFERENCIA = 95   # la cola por encima de este percentil queda en el ultimo intervalo abierto


def calcular_bordes(velocidades: np.ndarray, intervalos, umbral_calma: float) -> np.ndarray:
    """
    Bordes de los intervalos de velocidad. El primer borde es siempre umbral_calma.
    Si no se envian intervalos, se calculan valores 'redondos' segun los datos, tomando
    como referencia un percentil alto en lugar del maximo para que los valores extremos
    no ensanchen los intervalos.
    """
    if intervalos is None:
        v_ref = np.percentile(velocidades, PERCENTIL_REFERENCIA)
        if v_ref <= umbral_calma:
            return np.array([umbral_calma])
        intervalos = MaxNLocator(nbins=N_INTERVALOS_AUTO, steps=[1, 2, 2.5, 5, 10]).tick_values(umbral_calma, v_ref)
        intervalos = intervalos[intervalos < v_ref]

    bordes = [b for b in intervalos if b > umbral_calma]
    return np.array([umbral_calma] + bordes)


def calcular_frecuencias(direcciones, velocidades, n_sectores: int, bordes, umbral_calma: float):
    """
    Matriz [sector x intervalo] en % del total y el % de calmas.
    """
    total = len(velocidades)
    ancho = 360 / n_sectores

    # Desplazamiento de medio sector: el sector N queda centrado en 0° (360° equivale a 0°)
    sectores = (((direcciones + ancho / 2) % 360) // ancho).astype(int)
    calma = velocidades < umbral_calma
    intervalos = np.digitize(velocidades, bordes) - 1   # el ultimo intervalo queda abierto

    frecuencias = np.zeros((n_sectores, len(bordes)))
    np.add.at(frecuencias, (sectores[~calma], intervalos[~calma]), 1)

    return frecuencias * 100 / total, calma.sum() * 100 / total


class RosaVientosGrafico(BaseGrafico):

    PROYECCION = "polar"
    KWARGS_LEYENDA = {"loc": "center left", "bbox_to_anchor": (1.1, 0.5)}

    def __init__(self, estilo: EsteticaSchema):
        super().__init__(estilo)
        self.estilo_rosa = EstiloRosaVientos()

    def plot(self, ax: plt.Axes, peticion: PeticionRosaVientos) -> None:
        """
        Bloque de Dibujo: Implementa el BaseGrafico.
        Barras polares apiladas por intervalo de velocidad.
        La estetica especifica se delega a utils/estilo/estilo_rosa_vientos.py
        """
        estilo = self.estilo_rosa
        n = peticion.n_sectores
        direcciones = np.asarray(peticion.direcciones, dtype=float)
        velocidades = np.asarray(peticion.velocidades, dtype=float)

        bordes = calcular_bordes(velocidades, peticion.intervalos_velocidad, peticion.umbral_calma)
        frecuencias, porcentaje_calmas = calcular_frecuencias(
            direcciones, velocidades, n, bordes, peticion.umbral_calma
        )

        angulos = np.deg2rad(np.arange(n) * 360 / n)
        ancho = np.deg2rad(360 / n)
        colores = colores_por_intervalo(len(bordes), estilo)
        etiquetas = etiquetas_intervalos(bordes, peticion.unidades)

        acumulado = np.zeros(n)
        for j in range(len(bordes)):
            ax.bar(angulos, frecuencias[:, j], width=ancho, bottom=acumulado,
                   color=colores[j], label=etiquetas[j])
            acumulado += frecuencias[:, j]

        configurar_ejes_polares(ax, n)
        anotar_pie(ax, porcentaje_calmas, estilo)


def dibujar(peticion: PeticionRosaVientos) -> str:
    """
    Enrutamiento a api/router.py
    """
    graficador = RosaVientosGrafico(estilo=peticion.estetica)
    return graficador.render(peticion)
