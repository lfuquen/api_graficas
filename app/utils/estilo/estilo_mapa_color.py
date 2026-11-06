from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize


@dataclass(frozen=True)
class EstiloMapaColor:
    """
    Configuracion predeterminada institucional para mapas de color.
    Solo declara lo que difiere de la base de Matplotlib y de aplicar_estilo().
    """
    mapa_secuencial: str = "cmo.thermal"
    mapa_divergente: str = "cmo.balance"
    niveles: int = 12                 # niveles por defecto en modo contorno
    lineas_contorno: bool = True
    color_contorno: str = "k"
    grosor_contorno: float = 0.4
    alpha_contorno: float = 0.5


def mapa_colores(estilo: EstiloMapaColor, divergente: bool):
    return mpl.colormaps[estilo.mapa_divergente if divergente else estilo.mapa_secuencial]


def normalizacion(z: np.ma.MaskedArray, vmin, vmax, divergente: bool) -> Normalize:
    """
    Divergente: escala simetrica alrededor de 0 para que el color neutro coincida con el cero.
    Secuencial: vmin/vmax de la peticion o, si faltan, los de los datos.
    """
    if divergente:
        limites = [abs(v) for v in (vmin, vmax) if v is not None]
        limite = max(limites) if limites else float(np.abs(z).max())
        return Normalize(-limite, limite)
    return Normalize(vmin, vmax)


def agregar_barra_color(ax: plt.Axes, mappable, etiqueta: str, fuente) -> None:
    barra = ax.figure.colorbar(mappable, ax=ax, pad=0.02)
    if etiqueta:
        barra.set_label(etiqueta, fontproperties=fuente)
    barra.outline.set_visible(False)
