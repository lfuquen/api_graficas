import matplotlib.pyplot as plt
from graficadores.base_grafica import BaseGrafico
from schemas.schemas import PeticionDispersion


class DispersionGrafico(BaseGrafico):

    # Ajustes esteticos propios de dispersion (configuracion sencilla, sin archivo exclusivo en utils/estilo)
    ALPHA = 1
    COLOR_BORDE = "#0086D6"

    def plot(self, ax: plt.Axes, peticion: PeticionDispersion) -> None:
        """
        Bloque de Dibujo: Implementa el BaseGrafico.
        """
        var_x = peticion.variable_x
        var_y = peticion.variable_y

        ax.scatter(
            var_x.valores,
            var_y.valores,
            alpha=self.ALPHA,
            edgecolors=self.COLOR_BORDE
        )

        if not peticion.estetica.xlabel:
            label_x = f"{var_x.nombre} ({var_x.unidades})" if var_x.unidades else var_x.nombre
            ax.set_xlabel(label_x, fontproperties=self.props_tipograficas["etiquetas"])

        if not peticion.estetica.ylabel:
            label_y = f"{var_y.nombre} ({var_y.unidades})" if var_y.unidades else var_y.nombre
            ax.set_ylabel(label_y, fontproperties=self.props_tipograficas["etiquetas"])


def dibujar(peticion: PeticionDispersion) -> str:
    """
    Enrutamiento a api/router.py
    """
    graficador = DispersionGrafico(estilo=peticion.estetica)
    return graficador.render(peticion)