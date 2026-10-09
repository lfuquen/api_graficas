import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from .fuentes import registrar_fuentes, roles_tipograficos, FUENTE_PREDETERMINADA

# Valores pedeterminados institucionales
DPI_PREDETERMINADO = 300
FIGSIZE_PREDETERMINADO = (8, 5)

paleta_colores = [
    "#009BDE", "#1C3D71", "#0086D6", "#FFE800",
    "#E7531E", "#F29300", "#D22630", "#BABBBB", 
    "#DAD9D8", "#000000", "#FFE800", "#D22630"
]

colores_extra = [cm.viridis(i) for i in np.linspace(0, 1, 20)]
paleta_extendida = paleta_colores + colores_extra


# Asignación estándar de variaciones en parametros rc.

def aplicar_estilo(
    fuente: str = FUENTE_PREDETERMINADA,
    dpi: int = DPI_PREDETERMINADO,
    figsize: tuple = FIGSIZE_PREDETERMINADO,
    grid: bool = True,
    ajustes_roles: dict = None
    # overrides_rc: dict = None
) -> dict:
    """
    Aplica la configuración global de Matplotlib usando los estándares institucionales.
    
    - Asigna los parámetros por defecto (dpi, figsize, fuente, grid).
    - Permite modificar roles tipográficos mediante 'ajustes_roles'.
    - Permite sobreescribir cualquier clave de rcParams mediante 'overrides_rc'.
    - Retorna el diccionario 'tipografia' generado por fuentes.py.
    """

    registrar_fuentes(fuente)
    tipografia = roles_tipograficos(fuente=fuente, ajustes_roles=ajustes_roles)

    config_rc = {
        "figure.dpi": dpi,
        "figure.figsize": figsize,
        "font.family": fuente,
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.edgecolor": "#080808",
        "axes.linewidth": 1.2,
        "grid.color": "#DAD9D8",
        "grid.linestyle": "-",
        "grid.linewidth": 0.4,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
        "axes.prop_cycle": plt.cycler(color=paleta_extendida),
        "legend.frameon": True,
        "legend.fancybox": True,
        "legend.framealpha": 0.7,
        "legend.facecolor": "#F0F0F0",
        "legend.edgecolor": "#DAD9D8",
        "savefig.dpi": dpi,
        "axes.grid": bool(grid)
    }

    plt.rcParams.update(config_rc)
    return tipografia

def sincronizar_seaborn():
    """Sincroniza la paleta corporativa principal con Seaborn si está instalado."""
    try:
        import seaborn as sns
        sns.set_palette(paleta_colores)
    except Exception:
        pass