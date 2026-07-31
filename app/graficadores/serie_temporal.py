import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .base_grafica import BaseGrafico
from schemas.schemas import MensajeroExtractorSchema, InfoTecnicaSchema

class SerieTemporalGrafico(BaseGrafico):
    
    def _procesamiento_datos(self, fechas: list, datos_brutos: list, operaciones: list) -> pd.DataFrame:
        """
        Convierte las listas del mensajero en un DataFrame de Pandas
        y calcula las reducciones temporales y estadísticas solicitadas.
        """
        # Se crea el DataFrame base con indice de tiempo
        df = pd.DataFrame({"valor": datos_brutos}, index=pd.to_datetime(fechas))
        df_resultados = pd.DataFrame(index=df.index)
        
        # Se ejecutan las operaciones solicitadas por el usuario
        if "datos_brutos" in operaciones:
            df_resultados["Datos Brutos"] = df["valor"]
            
        if "promedio_diario" in operaciones:
            df_resultados["Promedio Diario"] = df["valor"].resample("D").transform("mean")
            
        if "promedio_mensual" in operaciones:
            df_resultados["Promedio Mensual"] = df["valor"].resample("ME").transform("mean")
            
        if "promedio_anual" in operaciones:
            df_resultados["Promedio Anual"] = df["valor"].resample("YE").transform("mean")
            
        if "maximos" in operaciones:
            df_resultados["Máximos"] = df["valor"].cummax() # O resample si es por bloques
            
        if "minimos" in operaciones:
            df_resultados["Mínimos"] = df["valor"].cummin()

        # Si el usuario no pidio operaciones validas, devolvemos al menos el bruto
        if df_resultados.empty:
            df_resultados["Datos"] = df["valor"]
            
        return df_resultados

    def plot(self, ax, mensajero: MensajeroExtractorSchema) -> None:
        """
        Bloque de Dibujo: Implementa obligatoriamente el metodo abstracto de BaseGrafico.
        """

        df_lineas = self._procesamiento_datos(
            mensajero.fechas,
            mensajero.datos_brutos,
            mensajero.config_usuario.operaciones)
        
        # Se itera sobre las columnas calculadas y graficarlas
        for columna in df_lineas.columns:
            ax.plot(
                df_lineas.index, 
                df_lineas[columna], 
                label=f"{columna} ({mensajero.info_tecnica.unidades_dataset})"
            )
            
        # Anotacion cientifica extra opcional en el lienzo (ej. coordenadas reales)
        ax.text(
            0.02, 0.02, 
            f"Lat real: {mensajero.info_tecnica.lat_real:.3f} | Lon real: {mensajero.info_tecnica.lon_real:.3f}",
            transform=ax.transAxes, 
            fontsize=8, 
            bbox=dict(boxstyle="round,pad=0.3", fc="#F0F0F0", edgecolor="#DAD9D8", alpha=0.8)
        )


def dibujar(mensajero: MensajeroExtractorSchema) -> str:
    """
   Funcion de enrutamiento para main.py
    """

    graficador = SerieTemporalGrafico(estilo=mensajero.config_usuario.estetica)    
    return graficador.render(mensajero)