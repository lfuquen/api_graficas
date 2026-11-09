"""
Genera las capas del mapa base recortadas a la extension terrestre y maritima de Colombia:
  - Natural Earth (tierra y costa, 10m y 50m), con la estructura que Cartopy espera.
  - Costa de alta resolucion DIMAR/CIOH, dividida en cuadriculas (costa_alta/).
Herramienta de mantenimiento: la API no la importa ni la ejecuta.

Uso, desde api_graficas con el entorno activo:
    python app/static/cartopy/recortar_shapefiles.py

Si los shapefiles completos de Natural Earth no estan en la cache de Cartopy (~/.local/share/cartopy),
se descargan (requiere internet solo esta vez). La costa DIMAR/CIOH original debe estar en
api_graficas/fuentes/Linea_Costa (excluida de git).
Para ampliar la region, modificar CAJA y volver a ejecutar.
"""
import shutil
from pathlib import Path
import numpy as np
import shapefile
import shapely
import cartopy.io.shapereader as shpreader
from shapely.geometry import box, shape, mapping
from shapely.ops import unary_union

DESTINO = Path(__file__).resolve().parent / "shapefiles/natural_earth/physical"

# Linea de costa de alta resolucion DIMAR/CIOH (poligonos de tierra, WGS84)
ORIGEN_COSTA_ALTA = Path(__file__).resolve().parents[3] / "fuentes/Linea_Costa/caribe-pacifico_2024_TajamarMagdalena.shp"
DESTINO_COSTA_ALTA = Path(__file__).resolve().parent / "costa_alta"
PASO_CUADRICULA = 0.5   # grados; el graficador solo lee las cuadriculas que tocan el mapa

# Colombia continental, San Andres y Providencia, Serranilla, Bajo Nuevo, Malpelo y aguas del Caribe y Pacifico
# lon_min, lat_min, lon_max, lat_max
CAJA = box(-86, -5, -65, 17)
CAPAS = [("10m", "land"), ("10m", "coastline"), ("50m", "land"), ("50m", "coastline")]
TIPOS_VALIDOS = {"Polygon", "MultiPolygon", "LineString", "MultiLineString"}


def recortar(origen: Path, destino: Path) -> int:
    lector = shapefile.Reader(str(origen))
    escritor = shapefile.Writer(str(destino), shapeType=lector.shapeType)
    escritor.fields = lector.fields[1:]

    n = 0
    for registro in lector.iterShapeRecords():
        geom = shape(registro.shape.__geo_interface__)
        if not geom.intersects(CAJA):
            continue
        recorte = geom.intersection(CAJA)
        if recorte.geom_type == "GeometryCollection":
            partes = [g for g in recorte.geoms if g.geom_type in TIPOS_VALIDOS]
            if not partes:
                continue
            recorte = unary_union(partes)   # descarta puntos sueltos que deja el corte en el borde
        if recorte.is_empty or recorte.geom_type not in TIPOS_VALIDOS:
            continue
        escritor.shape(mapping(recorte))
        escritor.record(*registro.record)
        n += 1
    escritor.close()

    for ext in (".prj", ".cpg"):
        if origen.with_suffix(ext).exists():
            shutil.copy(origen.with_suffix(ext), destino.with_suffix(ext))
    return n


def _cuadriculas(paso: float) -> list:
    x0, y0, x1, y1 = CAJA.bounds
    return [box(x, y, min(x + paso, x1), min(y + paso, y1))
            for x in np.arange(x0, x1, paso) for y in np.arange(y0, y1, paso)]


def _escribir(destino: Path, tipo: int, geometrias: list) -> None:
    escritor = shapefile.Writer(str(destino), shapeType=tipo)
    escritor.field("id", "N", 6, 0)
    for i, geom in enumerate(geometrias):
        escritor.shape(mapping(geom))
        escritor.record(i)
    escritor.close()
    shutil.copy(ORIGEN_COSTA_ALTA.with_suffix(".prj"), destino.with_suffix(".prj"))


def procesar_costa_alta() -> None:
    """
    Recorta la costa de alta resolucion a CAJA y la divide en cuadriculas en dos capas:
      - tierra: poligonos de tierra (relleno; sus bordes de cuadricula no se dibujan)
      - costa:  borde real de la tierra como lineas (sin los cortes artificiales de la cuadricula)
    Los atributos S-57 del original se descartan: es un unico registro disuelto y no describen la geometria.
    """
    original = shape(shapefile.Reader(str(ORIGEN_COSTA_ALTA)).shape(0).__geo_interface__)
    tierra = original.intersection(CAJA)
    costa = original.boundary.intersection(CAJA)
    shapely.prepare(tierra)
    shapely.prepare(costa)

    tierra_cuadriculas, costa_cuadriculas = [], []
    for celda in _cuadriculas(PASO_CUADRICULA):
        if tierra.intersects(celda):
            parte = tierra.intersection(celda)
            if parte.geom_type == "GeometryCollection":
                parte = unary_union([g for g in parte.geoms if g.geom_type in ("Polygon", "MultiPolygon")])
            if not parte.is_empty and parte.geom_type in ("Polygon", "MultiPolygon"):
                tierra_cuadriculas.append(parte)
        if costa.intersects(celda):
            parte = costa.intersection(celda)
            if parte.geom_type == "GeometryCollection":
                parte = unary_union([g for g in parte.geoms if g.geom_type in ("LineString", "MultiLineString")])
            if not parte.is_empty and parte.geom_type in ("LineString", "MultiLineString"):
                costa_cuadriculas.append(parte)

    DESTINO_COSTA_ALTA.mkdir(parents=True, exist_ok=True)
    _escribir(DESTINO_COSTA_ALTA / "tierra", shapefile.POLYGON, tierra_cuadriculas)
    _escribir(DESTINO_COSTA_ALTA / "costa", shapefile.POLYLINE, costa_cuadriculas)
    print(f"costa_alta: {len(tierra_cuadriculas)} cuadriculas de tierra, {len(costa_cuadriculas)} de costa")


if __name__ == "__main__":
    DESTINO.mkdir(parents=True, exist_ok=True)
    for escala, nombre in CAPAS:
        origen = Path(shpreader.natural_earth(resolution=escala, category="physical", name=nombre))
        n = recortar(origen, DESTINO / origen.stem)
        print(f"{origen.stem}: {n} geometrias")
    procesar_costa_alta()
