from dataclasses import dataclass
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

PUNTOS_CARDINALES = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"
]

TEXTOS_CONVENCION = {
    "procedencia": "Dirección de procedencia",
    "destino": "Dirección de destino"
}


@dataclass(frozen=True)
class EstiloRosaVientos:
    """
    Valores esteticos institucionales para rosas de vientos.
    Por ahora no se sobrescriben desde la peticion.
    """
    convencion: str = "procedencia"      # "procedencia" | "destino"
    mapa_colores: str = "cmocean"


def colores_por_intervalo(n_intervalos: int, estilo: EstiloRosaVientos) -> list:
    return mpl.colormaps[estilo.mapa_colores](np.linspace(0, 1, n_intervalos))


def etiquetas_intervalos(bordes, unidades: str) -> list:
    """
    '0.5–2 m/s', '2–4 m/s', ..., '≥8 m/s' (ultimo intervalo abierto).
    """
    etiquetas = [f"{a:g}–{b:g} {unidades}" for a, b in zip(bordes[:-1], bordes[1:])]
    etiquetas.append(f"≥{bordes[-1]:g} {unidades}")
    return etiquetas


def configurar_ejes_polares(ax: plt.Axes, n_sectores: int) -> None:
    """
    Norte arriba, sentido horario y puntos cardinales.
    """
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    n_etiquetas = 8 if n_sectores == 8 else 16
    paso = 16 // n_etiquetas
    ax.set_thetagrids(np.arange(n_etiquetas) * 360 / n_etiquetas, PUNTOS_CARDINALES[::paso])


def anotar_pie(ax: plt.Axes, porcentaje_calmas: float, estilo: EstiloRosaVientos) -> None:
    """
    Texto bajo la rosa con la convencion y el porcentaje de calmas.
    """
    texto = f"{TEXTOS_CONVENCION[estilo.convencion]}  ·  Calmas: {porcentaje_calmas:.1f}%"
    ax.text(0.5, -0.12, texto, transform=ax.transAxes, ha="center", va="top")
