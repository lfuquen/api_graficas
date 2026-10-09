import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from core.config import settings

# Archivos de imagen corporativos
LOGO_PRINCIPAL = "escudo_dimar_ver.png"
LOGO_SEGUNDARIO = "escudo_dimar_hor.png"  # Opción alternativa

# Configuración de marca de agua localicada (predetermanada en el centro)
def marca_agua_localizada(
    fig: plt.Figure, 
    logo_filename: str = LOGO_PRINCIPAL, 
    alpha: float = 0.12, 
    escala_relativa: float = 0.3, 
    margen_px: int = 10, 
    modo: str = "centro"  # Centro como ubicación predeterminada
) -> None:
   
    logo_path = os.path.join(settings.RUTA_LOGOS, logo_filename)

    if not os.path.exists(logo_path):
        print(f"Advertencia: Logo no encontrado en {logo_path}")
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

    if modo == "centro":
        xo = int((fig_w_px - target_w) / 2)
        yo = int((fig_h_px - target_h) / 2)
    elif modo == "inf_derecha":
        xo = int(fig_w_px - target_w - margen_px)
        yo = int(margen_px)
    elif modo == "inf_izquierda":
        xo = int(margen_px)
        yo = int(margen_px)
    elif modo == "sup_derecha":
        xo = int(fig_w_px - target_w - margen_px)
        yo = int(fig_h_px - target_h - margen_px)
    else:  # "sup_izquierda"
        xo = int(margen_px)
        yo = int(fig_h_px - target_h - margen_px)

    fig.figimage(logo_arr, xo=xo, yo=yo, alpha=alpha, zorder=10)

# Configuración de marca de agua en malla (opcional)
def marca_agua_malla(
    fig: plt.Figure, 
    logo_filename: str = LOGO_PRINCIPAL, 
    alpha: float = 0.12, 
    escala_relativa: float = 0.1, 
    spacing: int = 300
) -> None:

    logo_path = os.path.join(settings.RUTA_LOGOS, logo_filename)

    if not os.path.exists(logo_path):
        print(f"Advertencia: Logo no encontrado en {logo_path}")
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

    for xo in range(0, int(fig_w_px), spacing):
        for yo in range(0, int(fig_h_px), spacing):
            fig.figimage(logo_arr, xo=xo, yo=yo, alpha=alpha, zorder=10)


def aplicar_marca_agua(
    fig: plt.Figure, 
    modo: str = "localizada", 
    logo_filename: str = LOGO_PRINCIPAL,
    **kwargs
) -> None:
    """
    Fachada del módulo de marcas de agua.
    Si no se pasan argumentos, aplica la marca centrada institucional por defecto.
    """
    if modo == "malla":
        marca_agua_malla(fig, logo_filename=logo_filename, **kwargs)
    else:
        marca_agua_localizada(fig, logo_filename=logo_filename, modo=modo, **kwargs)