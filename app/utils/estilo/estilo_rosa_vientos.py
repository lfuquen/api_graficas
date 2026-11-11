from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

PUNTOS_CARDINALES = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"
]


@dataclass(frozen=True)
class EstiloRosaVientos:
    """
    Configuracion predeterminada institucional para rosas de vientos.
    Solo declara lo que difiere de la base de Matplotlib y de aplicar_estilo().
    """
    mapa_colores: str = "viridis"


def colores_por_intervalo(n_intervalos: int, estilo: EstiloRosaVientos) -> list:
    return mpl.colormaps[estilo.mapa_colores](np.linspace(0, 1, n_intervalos))


def configurar_ejes_polares(ax: plt.Axes, n_sectores: int) -> None:
    """
    Norte arriba, sentido horario y puntos cardinales.
    """
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    paso = 2 if n_sectores == 8 else 1
    ax.set_thetagrids(np.arange(16)[::paso] * 22.5, PUNTOS_CARDINALES[::paso])
