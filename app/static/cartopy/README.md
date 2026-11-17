# Capas del mapa base

Datos de tierra y línea de costa que usa el graficador `mapa_color` (Cartopy) para dibujar el mapa base
sin depender de internet. Las rutas se configuran en `core/config.py` (`RUTA_CARTOPY`, `RUTA_COSTA_ALTA`)
y se aplican en `utils/estilo/estilo_mapa_color.py`.

## Contenido

- `shapefiles/natural_earth/physical/`: capas de Natural Earth `ne_10m_land`, `ne_10m_coastline`,
  `ne_50m_land` y `ne_50m_coastline`. La estructura de carpetas es la que Cartopy espera; no cambiar
  nombres ni rutas.
- `costa_alta/`: línea de costa de alta resolución DIMAR/CIOH dividida en cuadrículas de 0,5°:
  - `tierra`: polígonos de tierra (relleno).
  - `costa`: borde real de la tierra como líneas (sin los cortes de la cuadrícula).
- `recortar_shapefiles.py`: herramienta de mantenimiento que genera todas las capas. La API no la importa
  ni la ejecuta.

## Qué capa se usa

El graficador elige según el lado mayor del mapa (`umbral_alta_resolucion` en `EstiloMapaColor`, 5° por
defecto):

| Lado mayor del mapa | Capa |
|---------------------|------|
| Menor que 5°        | Costa de alta resolución DIMAR/CIOH (detalle de puerto: muelles, escolleras, tajamares) |
| 5° o más            | Natural Earth 10m |

La costa de alta resolución se carga en memoria al iniciar la API, una vez por worker (`precargar_capas`
en `utils/estilo/estilo_mapa_color.py`); cada gráfica solo lee las cuadrículas que tocan el mapa.

## Región

Todas las capas están recortadas a la extensión terrestre y marítima de Colombia:

| Límite   | Valor |
|----------|-------|
| Longitud | -86 a -65 |
| Latitud  | -5 a 17 |

Incluye Colombia continental, San Andrés y Providencia, Serranilla, Bajo Nuevo, Malpelo y las aguas del
Caribe y del Pacífico. Una gráfica con coordenadas fuera de esta región se dibuja sin tierra ni costa en
la parte que queda por fuera, y se registra una advertencia en el log. La región está declarada también
en `REGION_MAPA_BASE` (`utils/estilo/estilo_mapa_color.py`); si se modifica `CAJA`, actualizarla.

## Regenerar o ampliar la región

1. Para la costa de alta resolución, ubicar el archivo original en
   `api_graficas/fuentes/Linea_Costa/caribe-pacifico_2024_TajamarMagdalena.shp`. Esta carpeta está
   excluida de git; el archivo se obtiene del repositorio interno de DIMAR/CIOH. Si cambia la edición,
   actualizar `ORIGEN_COSTA_ALTA` en `recortar_shapefiles.py`.
2. Para ampliar la región, modificar `CAJA` en `recortar_shapefiles.py`.
3. Desde `api_graficas`, con el entorno activo:

   ```bash
   python app/static/cartopy/recortar_shapefiles.py
   ```

Si los shapefiles completos de Natural Earth no están en la caché de Cartopy (`~/.local/share/cartopy`),
se descargan (requiere internet solo esa vez). El procesamiento de la costa de alta resolución tarda
alrededor de 40 s. Actualizar este README si cambia la región, la fuente o el umbral.

## Fuentes y licencias

- [Natural Earth](https://www.naturalearthdata.com/), dominio público.
- Línea de costa DIMAR/CIOH, edición 2024 (incluye la actualización del tajamar del río Magdalena).
  Uso institucional, sin restricciones para esta API.
