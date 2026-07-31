import os
import matplotlib.pyplot as plt
from PIL import Image
from app.utils.estilo import aplicar_estilo, agregar_marca_agua
from core.config import settings

ruta_salidas = settings.SALIDAS_GRAFICAS

def _crear_fig_ax(figsize=None, fuente="helvetica"):
    estilos = aplicar_estilo(fuente=fuente)
    if figsize:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = plt.subplots()
    return fig, ax


# # # Definicion de graficas segun el tipo, aplicando la configuracion de estilo
 
def grafica_lineas(x, y, titulo="", xlabel="", ylabel="", logo_filename="escudo_dimar_ver.png", figsize=None, dpi=300, nombre_archivo_salida=None):
    fig, ax = _crear_fig_ax (figsize=figsize)
    ax.plot(x, y, marker="")
    ax.set_title(titulo)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend (y)
    ax.grid(True)
    agregar_marca_agua(fig, logo_filename)
    if nombre_archivo_salida is not None:
        fig.savefig(os.path.join(ruta_salidas, nombre_archivo_salida), dpi=dpi)
    return fig, ax
print('Grafica de lineas definida exitosamente')


def grafica_barras(x, y, titulo="",xlabel="", ylabel="", logo_filename="escudo_dimar_ver.png", figsize=None, guardar=None, dpi=300):
    fig, ax = _crear_fig_ax(figsize=figsize)
    ax.bar(x, y)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    agregar_marca_agua(fig, logo_filename)
    if guardar:
        fig.savefig(guardar = "/home/lfuquen/cioh_26/api_graficas/salidas", dpi=dpi)
    return fig, ax
print('Grafica de barras definida exitosamente')

def grafica_dispersion(x, y, titulo="", xlabel="", ylabel="", logo_filename="escudo_dimar_ver.png", figsize=None, guardar=None, dpi=300):
    fig, ax = _crear_fig_ax(figsize)
    ax.scatter(x, y)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    agregar_marca_agua(fig, logo_filename)
    if guardar:
        fig.savefig(guardar = "./salidas/", dpi=dpi)
    return fig, ax
print('Grafica de dispersion definida exitosamente')



