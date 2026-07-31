# style_config.py
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.cm as cm
from PIL import Image
import numpy as np
from core.config import settings


#  definicion de la paleta de colores personalizada
paleta_colores = [
    "#009BDE", "#1C3D71", "#0086D6", "#FFE800",
    "#E7531E", "#F29300", "#D22630", "#BABBBB", 
    "#DAD9D8", "#000000", "#FFE800", "#0086D6", "#D22630"
]

colores_extra = [cm.viridis(i) for i in np.linspace(0, 1, 20)]
paleta_extendida = paleta_colores + colores_extra

#  definicion de las rutas de fuentes disponibles

ruta_fuentes = settings.RUTA_FUENTES

fuentes_disponibles = {
    "arial" : {
        "regular": os.path.join(ruta_fuentes, "arial.ttf"),
        "bold": os.path.join(ruta_fuentes, "arialbd.ttf"),
        "italic": os.path.join(ruta_fuentes, "ariali.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "arialbi.ttf")
    },
    "eurostile" : {
        "regular": os.path.join(ruta_fuentes, "eurostile.ttf"),
        "bold": os.path.join(ruta_fuentes, "eurostile_boldregular.ttf"),
        "italic": os.path.join(ruta_fuentes, "helvetica_oblique.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "helvetica_compressed.ttf")
    },
    "FiraSans" :{
        "regular": os.path.join(ruta_fuentes, "firasans_regular.ttf"),
        "bold": os.path.join(ruta_fuentes, "firasans_ultra.ttf"),
        "italic": os.path.join(ruta_fuentes, "firasans_extrabolditalic.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "firasans_bolditalic.ttf")
    },
    "helvetica" : {
        "regular": os.path.join(ruta_fuentes, "helvetica.ttf"),
        "bold": os.path.join(ruta_fuentes, "helvetica_bold.ttf"),
        "italic": os.path.join(ruta_fuentes, "helvetica_oblique.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "helvetica_compressed.otf")
    }}

#  registro de todas las variantes de la fuente registrada
def registrar_fuentes(fuente):
    if fuente not in fuentes_disponibles:
        raise ValueError(f"Fuente {fuente} no definida en fuentes_disponibles.")
    for estilo, ruta in fuentes_disponibles[fuente].items():
        if os.path.exists(ruta):
            fm.fontManager.addfont(ruta)
        else:
            print(f"Ruta de fuente no encontrada:{ruta}")


#  definicion de un diccionario de estilos tipograficos para la fuente seleccionada
def roles_tipograficos(fuente):
    estilos_fuente = fuentes_disponibles[fuente]
    estilos = {
        "titulo": fm.FontProperties(fname=estilos_fuente.get("bold")),
        "subtitulo": fm.FontProperties(fname=estilos_fuente.get("bold_italic")),
        "ticks": fm.FontProperties(fname=estilos_fuente.get("italic")),
        "etiquetas": fm.FontProperties(fname=estilos_fuente.get("italic")),
        "leyenda": fm.FontProperties(fname=estilos_fuente.get("regular")),
    }
    return estilos


#  definicion de parametros de estilo para las graficas
def aplicar_estilo(fuente="helvetica", dpi=300, figsize=(8, 6), grid=True):

    #  registrar fuentes
    registrar_fuentes(fuente)
    estilos = roles_tipograficos(fuente)

    plt.rcParams.update({
        "figure.dpi": 300,
        "figure.figsize": (8, 5 ),
        "font.family": "helvetica",
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
        "savefig.dpi": 300
    })
    plt.rcParams["axes.grid"] = bool(grid)

    return estilos

def sincronizar_seaborn():
   try:
       import seaborn as sns
       sns.set_palette(paleta_colores)
   except Exception:
       pass


"""
Se definen los tipos de marcas de agua disponibles
"""

# ##  Definición de la marca de agua en malla

def marca_agua_malla(fig, logo_filename='escudo_dimar_ver.png', alpha=0.12, escala_relativa=0.1, spacing=300):

    logo_path = os.path.join(settings.RUTA_LOGOS, logo_filename)

    if not os.path.exists(logo_path):
        print(f"Logo no encontrado en {logo_path}" )
        return
    
    logo_img = Image.open(logo_path).convert("RGBA")
    try:
        fig.canvas.draw()  # fuerza el layout antes de medir
    except Exception:
        pass
    
    fig_w_px = int(round(fig.get_size_inches()[0] * fig.get_dpi()))
    fig_h_px = int(round(fig.get_size_inches()[1] * fig.get_dpi()))
   
    original_w, original_h = logo_img.size
    target_w = int(fig_w_px * escala_relativa)
    target_h = int(target_w * (original_h / original_w))
    logo_resized = logo_img.resize((max(1, target_w), max(1, target_h)), Image.LANCZOS)
    logo_arr = np.asarray(logo_resized)

    for xo in range(0, int(fig_w_px), spacing):
        for yo in range(0, int(fig_h_px), spacing):
            fig.figimage(logo_arr, xo=xo, yo=yo, alpha=alpha, zorder=10)
    

# ## Definición de la marca de agua en un punto especifico

def marca_agua_localizada(fig, logo_filename="escudo_dimar_ver.png", alpha=0.12, escala_relativa=0.3, margen_px=10, esquina=""):     #ubicacion en específica

    logo_path = os.path.join(settings.RUTA_LOGOS, logo_filename)

    if not os.path.exists(logo_path):
        print(f"Logo no encontrado en {logo_path}" )
        return
    
    logo_img = Image.open(logo_path).convert("RGBA")
    try:
        fig.canvas.draw() 
    except Exception:
        pass

    fig_w_px = int(round(fig.get_size_inches()[0] * fig.get_dpi()))
    fig_h_px = int(round(fig.get_size_inches()[1] * fig.get_dpi()))

    original_w, original_h = logo_img.size
    target_w = int(fig_w_px * escala_relativa)
    target_h = int(target_w * (original_h / original_w))
    logo_resized = logo_img.resize((max(1, target_w), max(1, target_h)), Image.LANCZOS)
    logo_arr = np.asarray(logo_resized)

    if esquina == "centro":
        xo = int ((fig_w_px - target_w) / 2)
        yo = int ((fig_h_px - target_h) / 2)
    elif esquina == "inf_derecha":
       xo = int(fig_w_px - target_w - margen_px)
       yo = int(margen_px)
    elif esquina == "inf_izquierda":
       xo = int(margen_px)
       yo = int(margen_px)
    elif esquina == "sup_derecha":
       xo = int(fig_w_px - target_w - margen_px)
       yo = int(fig_h_px - target_h - margen_px)
    else: 
       xo = int(margen_px)
       yo = int(fig_h_px - target_h - margen_px)
    fig.figimage(logo_arr, xo=xo, yo=yo, alpha=alpha, zorder=10)
