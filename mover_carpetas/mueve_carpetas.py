"""Librerías para administrar directorios y
manipulación de imágenes
"""
from glob import glob
from pathlib import Path

import cv2 as cv


def cambiar_tamano(imagen, cambio: float):
    """Cambia el tamaño de una imagen con
    un factor de proporción

    Args:
        imagen (imagen): Imagen a cambiar.
        cambio (float): Factor de cambio de tamaño
        0 < cambio < 1 = reducción
        cambio > 1 = aumento

    Returns:
        imagen: Imagen con el tamaño cambiado.
    """
    alto, ancho, _ = imagen.shape
    # Redondea los nuevos tamaños a un valor entero
    ancho = int(ancho * cambio)
    alto = int(alto * cambio)
    return cv.resize(imagen, (ancho, alto), interpolation=cv.INTER_AREA)


def creador_carpetas(archivo: str) -> str:
    """Crea las carpetas de destino para los archivos.

    Args:
        archivo (str): Dirección del archivo.

    Returns:
        str: nombre del archivo con extensión y su nueva dirección.
    """
    # Extrae la dirección, el nombre del archivo y del alumne
    archivo = Path(archivo)
    nombre_archivo = archivo.name
    nombre_alumne = " ".join(nombre_archivo.split()[:-1])
    carpeta_padre = archivo.parent

    # Nombres de las carpetas nuevas
    nueva_carpeta = carpeta_padre.with_name(f"{carpeta_padre.name} Carpetas")
    carpeta_alumne = nueva_carpeta / nombre_alumne

    # Crea las nuevas carpetas sino existen
    carpeta_alumne.mkdir(parents=True, exist_ok=True)
    print(f"Procesando la carpeta de {nombre_alumne}")

    # Crea la nueva dirección del archivo
    nueva_direccion = carpeta_alumne / nombre_archivo
    return nombre_archivo, nueva_direccion.as_posix()


def main():
    """Función principal"""
    # archivos = Path(input("Nombre de la carpeta: ")).glob(r"*.JPG")
    archivos = glob(input("Nombre de la carpeta: ") + r"\*.JPG")
    reduccion = float(input("Rango de reducción (0 < x < 1 ): "))

    for archivo in archivos:
        # Crea las carpetas necesarias
        nombre_archivo, nueva_dirección = creador_carpetas(archivo)

        # Lee la imagen y la reduce
        img = cambiar_tamano(cv.imread(archivo), reduccion)

        # Guarda la imagen en la nueva dirección
        cv.imwrite(nueva_dirección, img)
        print(f"Copiado {nombre_archivo} reducido al {reduccion:.2%}.")

    input(f"Terminado procesado de {len(archivos)} archivos...")


if __name__ == "__main__":
    main()
