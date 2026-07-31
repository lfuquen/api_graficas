#import os
import numpy as np 
import pandas as pd

from graficadores.base_grafica import BaseGrafico
from schemas.schemas import MensajeroExtractorSchema
from utils.estilo import paleta_colores

class DispersionGrafico(BaseGrafico):
    """
    Graficador especializado para gráficos de dispersión.

    Soporta dos escenarios:
    1. Dispersión temporal: fechas vs una variable.
    2. Dispersión bi-variable: variable_x vs variable_y.
    """

    def plot(self, ax, mensajero: MensajeroExtractorSchema) -> None:
        variables = mensajero.info_tecnica.variables

        if len(variables) == 1:
            self._plot_dispersion_temporal(ax, mensajero, variables[0])

        elif len(variables) == 2:
            self._plot_dispersion_bivariable(ax, mensajero, variables[0], variables[1])

        else:
            raise ValueError("El gráfico de dispersión solo soporta una variable con fechas"
                             "o dos variables para dispersión bi-variable")

    def _plot_dispersion_temporal(self, ax, mensajero: MensajeroExtractorSchema, variable: str) -> None:

        """
        Dispersión temporal: tiempo vs variable (fechas vs valores de una variable)
        """

        if variable not in mensajero.datos_brutos:
            raise ValueError(f"La variable '{variable}' no existe en datos_brutos")

        if not mensajero.fechas:
            raise ValueError("Para dispersión temporal se requiere la llave 'fechas'")

        valores = mensajero.datos_brutos[variable].valores

        y_raw = np.array(valores, dtype=float).flatten()
        x_raw = pd.to_datetime(mensajero.fechas)

        if len(x_raw) != len(y_raw):
            raise ValueError("La cantidad de fechas no coincide con la cantidad de valores: "
                f"fechas={len(x_raw)} vs valores={len(y_raw)}"
            )

        mascara_valida = np.isfinite(y_raw)

        x_datos = x_raw[mascara_valida]
        y_datos = y_raw[mascara_valida]

        if len(y_datos) == 0:
            raise ValueError("No hay datos válidos para construir la dispersión temporal")

        color_puntos = paleta_colores[0]

        ax.scatter(
            x_datos,
            y_datos,
            color=color_puntos,
            alpha=0.7,
            edgecolors="none",
            s=40,
            label=variable
        )

    def _plot_dispersion_bivariable(self, ax, mensajero: MensajeroExtractorSchema, variable_x: str, variable_y: str) -> None:
        """
        Dispersión bi-variable: variable vs variable
        """

        if variable_x not in mensajero.datos_brutos:
            raise ValueError(
                f"La variable '{variable_x}' no existe en datos_brutos."
            )

        if variable_y not in mensajero.datos_brutos:
            raise ValueError(
                f"La variable '{variable_y}' no existe en datos_brutos."
            )

        valores_x = mensajero.datos_brutos[variable_x].valores
        valores_y = mensajero.datos_brutos[variable_y].valores

        x_raw = np.array(valores_x, dtype=float)
        y_raw = np.array(valores_y, dtype=float)

        if x_raw.shape != y_raw.shape:
            raise ValueError(
                "Las variables para dispersión no tienen dimensiones compatibles: "
                f"{variable_x} {x_raw.shape} vs {variable_y} {y_raw.shape}"
            )

        x_datos = x_raw.flatten()
        y_datos = y_raw.flatten()

        mascara_valida = np.isfinite(x_datos) & np.isfinite(y_datos)

        x_datos = x_datos[mascara_valida]
        y_datos = y_datos[mascara_valida]

        if len(x_datos) == 0:
            raise ValueError(
                "No hay datos válidos para construir la dispersión bi-variable."
            )

        color_puntos = paleta_colores[0]

        ax.scatter(
            x_datos,
            y_datos,
            color=color_puntos,
            alpha=0.7,
            edgecolors="none",
            s=40,
            label=f"{variable_x} vs {variable_y}"
        )


def dibujar(mensajero: MensajeroExtractorSchema):
    grafica = DispersionGrafico(mensajero.config_usuario.estetica)
    return grafica.render(mensajero)