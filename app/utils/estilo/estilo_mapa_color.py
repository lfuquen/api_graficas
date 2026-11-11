import logging
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
import shapefile
from shapely import STRtree
from shapely.geometry import box, shape
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import FuncFormatter, MaxNLocator
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from core.config import settings

# Shapefiles de Natural Earth incluidos en el proyecto: el servidor no depende de internet
cartopy.config["pre_existing_data_dir"] = str(settings.RUTA_CARTOPY)

CRS_DATOS = ccrs.PlateCarree()   # x, y de la peticion en grados: longitud [-180, 180], latitud

# Region cubierta por las capas de static/cartopy (debe coincidir con CAJA en recortar_shapefiles.py)
REGION_MAPA_BASE = (-86.0, -65.0, -5.0, 17.0)   # lon_min, lon_max, lat_min, lat_max

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EstiloMapaColor:
    """
    Configuracion predeterminada institucional para mapas de color.
    Solo declara lo que difiere de la base de Matplotlib y de aplicar_estilo().
    """
    mapa_secuencial: str = "turbo"
    mapa_divergente: str = "cmo.balance"
    niveles: int = 12                 # niveles por defecto en modo contorno
    lineas_contorno: bool = False
    color_contorno: str = "k"
    grosor_contorno: float = 0.4
    alpha_contorno: float = 0.5

    # Mapa base
    escala_costa: str = "10m"         # Natural Earth: "10m" (detalle regional) o "50m"
    umbral_alta_resolucion: float = 5.0   # grados; si el lado mayor del mapa es menor, usa la costa DIMAR/CIOH
    color_tierra: str = "#d9d9d9"
    color_costa: str = "#4d4d4d"
    grosor_costa: float = 0.6
    color_rejilla: str = "#808080"
    grosor_rejilla: float = 0.4
    estilo_rejilla: str = "--"
    max_marcas: int = 6               # maximo de marcas de coordenadas por eje


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


def _formato_lon(valor, _pos) -> str:
    if valor == 0 or abs(valor) == 180:
        return f"{abs(valor):g}°"
    return f"{abs(valor):g}°{'O' if valor < 0 else 'E'}"


def _formato_lat(valor, _pos) -> str:
    if valor == 0:
        return "0°"
    return f"{abs(valor):g}°{'S' if valor < 0 else 'N'}"


def _limites(valores: np.ndarray, media_celda: bool) -> tuple:
    """
    Limites de un eje (al menos 2 valores, lo garantiza el schema). Con media_celda (modo celdas)
    se amplian medio paso a cada lado, porque pcolormesh dibuja cada celda centrada en su coordenada.
    """
    v = np.sort(valores)
    if not media_celda:
        return v[0], v[-1]
    return v[0] - (v[1] - v[0]) / 2, v[-1] + (v[-1] - v[-2]) / 2


@lru_cache(maxsize=None)
def _capa_alta_resolucion(nombre: str) -> tuple:
    """
    Carga una sola vez (primera grafica que la necesite) las cuadriculas de la capa y su indice espacial.
    """
    lector = shapefile.Reader(str(settings.RUTA_COSTA_ALTA / nombre))
    geometrias = [shape(s.__geo_interface__) for s in lector.iterShapes()]
    return geometrias, STRtree(geometrias)


def _geometrias_alta_resolucion(nombre: str, extension: list) -> list:
    """
    Solo las cuadriculas que tocan la extension del mapa.
    """
    geometrias, indice = _capa_alta_resolucion(nombre)
    lon0, lon1, lat0, lat1 = extension
    return [geometrias[i] for i in indice.query(box(lon0, lat0, lon1, lat1))]


def _capas_costa(extension: list, estilo: EstiloMapaColor) -> tuple:
    """
    Mapas pequenos (lado mayor < umbral): costa de alta resolucion DIMAR/CIOH.
    Regiones amplias: Natural Earth.
    """
    lado_mayor = max(extension[1] - extension[0], extension[3] - extension[2])
    if lado_mayor < estilo.umbral_alta_resolucion:
        return (cfeature.ShapelyFeature(_geometrias_alta_resolucion("tierra", extension), CRS_DATOS),
                cfeature.ShapelyFeature(_geometrias_alta_resolucion("costa", extension), CRS_DATOS))
    return (cfeature.LAND.with_scale(estilo.escala_costa),
            cfeature.COASTLINE.with_scale(estilo.escala_costa))


def configurar_mapa_base(ax: plt.Axes, x: np.ndarray, y: np.ndarray,
                         estilo: EstiloMapaColor, fuente, media_celda: bool) -> None:
    """
    Extension segun los datos, tierra y costa por encima de los datos (tapan celdas sobre tierra)
    y rejilla con coordenadas en español (O/E, N/S).
    """
    extension = [*_limites(x, media_celda), *_limites(y, media_celda)]
    ax.set_extent(extension, crs=CRS_DATOS)

    lon0, lon1, lat0, lat1 = REGION_MAPA_BASE
    if extension[0] < lon0 or extension[1] > lon1 or extension[2] < lat0 or extension[3] > lat1:
        logger.warning("Mapa %s fuera de la region del mapa base %s: esa parte se dibuja sin tierra ni costa",
                       [round(float(v), 2) for v in extension], REGION_MAPA_BASE)

    tierra, costa = _capas_costa(extension, estilo)
    # Borde del mismo color que el relleno: oculta las uniones entre cuadriculas de la costa de alta resolucion
    ax.add_feature(tierra, facecolor=estilo.color_tierra, edgecolor=estilo.color_tierra,
                   linewidth=0.5, zorder=2)
    ax.add_feature(costa, facecolor="none", edgecolor=estilo.color_costa,
                   linewidth=estilo.grosor_costa, zorder=3)

    rejilla = ax.gridlines(crs=CRS_DATOS, draw_labels=True, color=estilo.color_rejilla,
                           linewidth=estilo.grosor_rejilla, linestyle=estilo.estilo_rejilla, zorder=4)
    rejilla.top_labels = False
    rejilla.right_labels = False
    rejilla.xlocator = MaxNLocator(nbins=estilo.max_marcas, steps=[1, 2, 2.5, 5, 10])
    rejilla.ylocator = MaxNLocator(nbins=estilo.max_marcas, steps=[1, 2, 2.5, 5, 10])
    rejilla.xformatter = FuncFormatter(_formato_lon)
    rejilla.yformatter = FuncFormatter(_formato_lat)
    rejilla.xlabel_style = {"fontproperties": fuente}
    rejilla.ylabel_style = {"fontproperties": fuente}
