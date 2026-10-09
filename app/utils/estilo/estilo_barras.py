from dataclasses import dataclass, fields
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class EstiloBarras:
    """
    Valores esteticos institucionales para graficos de barras.
    Cualquier campo puede sobrescribirse desde la peticion (EsteticaBarrasSchema).
    """
    ancho_barra: float = 0.8
    color_borde: str = "#1C3D71"
    grosor_borde: float = 0.5
    alpha: float = 1.0
    mostrar_valores: bool = False
    formato_valores: str = "%.1f"
    tamano_valores: int = 8
    rotacion_etiquetas: int = 0
    rejilla_eje_valores: bool = True

    @classmethod
    def desde_estetica(cls, estetica) -> "EstiloBarras":
        """
        Parte de los valores predeterminados y sobrescribe solo los campos
        que la peticion envio explicitamente (distintos de None).
        """
        ajustes = {
            f.name: getattr(estetica, f.name)
            for f in fields(cls)
            if getattr(estetica, f.name, None) is not None
        }
        return cls(**ajustes)


def kwargs_barra(estilo: EstiloBarras) -> dict:
    """
    Parametros comunes para ax.bar / ax.barh.
    """
    return {
        "edgecolor": estilo.color_borde,
        "linewidth": estilo.grosor_borde,
        "alpha": estilo.alpha,
    }


def anotar_valores(ax: plt.Axes, barras, estilo: EstiloBarras, apiladas: bool) -> None:
    if not estilo.mostrar_valores:
        return
    ax.bar_label(
        barras,
        fmt=estilo.formato_valores,
        label_type="center" if apiladas else "edge",
        padding=2,
        fontsize=estilo.tamano_valores
    )


def configurar_rejilla(ax: plt.Axes, horizontal: bool, estilo: EstiloBarras) -> None:
    """
    Rejilla solo en el eje de valores (o la global de rcparams si se desactiva).
    """
    if not estilo.rejilla_eje_valores:
        return
    ax.grid(False)
    ax.grid(True, axis="x" if horizontal else "y")


def configurar_categorias(ax: plt.Axes, posiciones, categorias, horizontal: bool, estilo: EstiloBarras) -> None:
    if horizontal:
        ax.set_yticks(posiciones)
        ax.set_yticklabels(categorias)
        ax.invert_yaxis()  # Primera categoria arriba
    else:
        ax.set_xticks(posiciones)
        ax.set_xticklabels(
            categorias,
            rotation=estilo.rotacion_etiquetas,
            ha="right" if estilo.rotacion_etiquetas else "center"
        )
