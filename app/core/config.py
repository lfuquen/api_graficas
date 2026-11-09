from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # - Variables con valores estaticos
    DIR_BASE: Path = Path(__file__).parent.parent
    RUTA_LOGOS: Path = Path(__file__).parent.parent  / "static/logos"
    RUTA_FUENTES: Path = Path(__file__).parent.parent  / "static/fonts"
    RUTA_CARTOPY: Path = Path(__file__).parent.parent  / "static/cartopy"
    RUTA_COSTA_ALTA: Path = Path(__file__).parent.parent  / "static/cartopy/costa_alta"
    CARGA_DATOS: Path = Path(__file__).parent.parent / "data"
    SALIDAS_GRAFICAS: Path = Path(__file__).parent.parent / "salidas" 
    

settings = Settings()
