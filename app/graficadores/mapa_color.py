import numpy as np
import matplotlib.pyplot as plt
from graficadores.base_grafica import BaseGrafico
from schemas.schemas import PeticionMapaColor, EsteticaSchema
from utils.estilo import (
    EstiloMapaColor,
    CRS_DATOS,
    mapa_colores,
    normalizacion,
    agregar_barra_color,
    configurar_mapa_base
)


class MapaColorGrafico(BaseGrafico):

    PROYECCION = CRS_DATOS   # GeoAxes de Cartopy; solo este graficador, BaseGrafico no cambia

    def __init__(self, estilo: EsteticaSchema):
        super().__init__(estilo)
        self.estilo_mapa = EstiloMapaColor()

    def plot(self, ax: plt.Axes, peticion: PeticionMapaColor) -> None:
        """
        Bloque de Dibujo: Implementa el BaseGrafico.
        Celdas (pcolormesh) o contornos rellenos (contourf) sobre una malla regular.
        La estetica especifica se delega a utils/estilo/estilo_mapa_color.py
        """
        estilo = self.estilo_mapa
        x = np.asarray(peticion.x, dtype=float)
        y = np.asarray(peticion.y, dtype=float)
        z = np.ma.masked_invalid(np.asarray(peticion.z, dtype=float))   # None -> NaN -> celda sin color

        cmap = mapa_colores(estilo, peticion.divergente)
        norm = normalizacion(z, peticion.vmin, peticion.vmax, peticion.divergente)

        if peticion.tipo == "contorno":
            malla = ax.contourf(x, y, z, levels=peticion.niveles or estilo.niveles,
                                cmap=cmap, norm=norm, transform=CRS_DATOS)
            if estilo.lineas_contorno:
                ax.contour(x, y, z, levels=malla.levels, colors=estilo.color_contorno,
                           linewidths=estilo.grosor_contorno, alpha=estilo.alpha_contorno,
                           transform=CRS_DATOS)
        else:
            malla = ax.pcolormesh(x, y, z, cmap=cmap, norm=norm, shading="auto", transform=CRS_DATOS)

        configurar_mapa_base(ax, x, y, estilo, self.props_tipograficas["etiquetas"],
                             media_celda=peticion.tipo == "celdas")
        agregar_barra_color(ax, malla, peticion.unidades, self.props_tipograficas["etiquetas"])


def dibujar(peticion: PeticionMapaColor) -> bytes:
    """
    Enrutamiento a api/router.py
    """
    graficador = MapaColorGrafico(estilo=peticion.estetica)
    return graficador.render(peticion)
