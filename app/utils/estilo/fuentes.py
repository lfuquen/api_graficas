import os
import matplotlib.font_manager as fm
from core.config import settings

ruta_fuentes = settings.RUTA_FUENTES
FUENTE_PREDETERMINADA = "helvetica"

fuentes_disponibles = {
    "arial": {
        "regular": os.path.join(ruta_fuentes, "arial.ttf"),
        "bold": os.path.join(ruta_fuentes, "arialbd.ttf"),
        "italic": os.path.join(ruta_fuentes, "ariali.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "arialbi.ttf")
    },
    "eurostile": {
        "regular": os.path.join(ruta_fuentes, "eurostile.ttf"),
        "bold": os.path.join(ruta_fuentes, "eurostile_boldregular.ttf"),
        "italic": os.path.join(ruta_fuentes, "helvetica_oblique.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "helvetica_compressed.ttf")
    },
    "FiraSans": {
        "regular": os.path.join(ruta_fuentes, "firasans_regular.ttf"),
        "bold": os.path.join(ruta_fuentes, "firasans_ultra.ttf"),
        "italic": os.path.join(ruta_fuentes, "firasans_extrabolditalic.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "firasans_bolditalic.ttf")
    },
    "helvetica": {
        "regular": os.path.join(ruta_fuentes, "helvetica.ttf"),
        "bold": os.path.join(ruta_fuentes, "helvetica_bold.ttf"),
        "italic": os.path.join(ruta_fuentes, "helvetica_oblique.ttf"),
        "bold_italic": os.path.join(ruta_fuentes, "helvetica_compressed.otf")
    }
}

"""
Asignación estándar de variante tipográfica por rol.
En esta sección modifica la tipografía para cada rol.
"""
MAPEO_ROLES_PREDETERMINADO = {
    "titulo": "bold",
    "subtitulo": "bold_italic",
    "ticks": "italic",
    "etiquetas": "italic",
    "leyenda": "regular"
}

def registrar_fuentes(fuente: str = MAPEO_ROLES_PREDETERMINADO):
    """Registra en Matplotlib todas las variantes de la fuente seleccionada."""
    if fuente not in fuentes_disponibles:
        raise ValueError(f"Fuente '{fuente}' no definida en fuentes_disponibles.")
    
    for estilo, ruta in fuentes_disponibles[fuente].items():
        if os.path.exists(ruta):
            fm.fontManager.addfont(ruta)
        else:
            print(f"Advertencia: Ruta de fuente no encontrada en {ruta}")


def roles_tipograficos(
    fuente: str = MAPEO_ROLES_PREDETERMINADO, 
    ajustes_roles: dict = None #
) -> dict:
    """
    Genera los objetos FontProperties para cada rol.
    """
    if fuente not in fuentes_disponibles:
        raise ValueError(f"Fuente '{fuente}' no definida en fuentes_disponibles.")

    estilos_fuente = fuentes_disponibles[fuente]
    
    mapeo_activo = MAPEO_ROLES_PREDETERMINADO.copy()
    
    if ajustes_roles:
        mapeo_activo.update(ajustes_roles)

    tipografia = {}
    for rol, variante in mapeo_activo.items():
        ruta_archivo = estilos_fuente.get(variante)
    
        if not ruta_archivo or not os.path.exists(ruta_archivo):
            ruta_archivo = estilos_fuente.get("regular")

        tipografia[rol] = fm.FontProperties(fname=ruta_archivo)

    return tipografia