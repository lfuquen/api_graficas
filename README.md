# API de productos graficos de SOMO

API para la generación de los productos gráficos de SOMO según los estandares institucionales de DIMAR 

## Para correr la aplicacion

1. Ubicarse en la carpeta principal de la aplicacion (`api_graficas`)
2. Ejecutar (activa el entorno `graficador_env` y lanza uvicorn):

   ```bash
   bash run_server-dev.sh
   ```

Alternativa manual, desde `api_graficas`:

```bash
source graficador_env/bin/activate
uvicorn app.main:app --reload
```

## Tener en cuenta cada vez

- Lanzar siempre desde `api_graficas`: de ahi depende encontrar `app.main`.
- Los endpoints de graficos responden directamente con la imagen PNG (`Content-Type: image/png`); la API no guarda archivos en disco.
- El entorno del proyecto es `graficador_env`. Si cambia de nombre o ubicacion, actualizar la ruta en `run_server-dev.sh`.
- Si falta una libreria, con el entorno activo: `pip install -r requirements.txt`
- Por defecto la API queda en http://127.0.0.1:8000 y la documentacion en `/docs`.
- Para detener el servidor: `Ctrl+C`.

## Opcional

Una sola vez, para poder lanzar el script con `./run_server-dev.sh`:

```bash
chmod +x run_server-dev.sh
```
