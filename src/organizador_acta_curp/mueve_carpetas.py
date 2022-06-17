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


def crear_destino(archivo: str) -> Path:
    """Crea las carpetas de destino para un archivo.

    Args:
        archivo (str): Dirección del archivo.

    Returns:
        Path: Dirección final del archivo con su nuevo nombre.
    """
    # Extrae la dirección, el nombre del archivo y del alumne
    archivo = Path(archivo)

    # Salva el nombre de la carpeta padre y el archivo
    carpeta_padre_in, nombre_archivo = archivo.parent, archivo.name

    # Extrae el nombre del alumne
    nombre_alumne = " ".join(nombre_archivo.split()[:-1])

    # Determina la ubicación de la carpeta del alumne
    carpeta_padre_out = carpeta_padre_in.with_name(f"{carpeta_padre_in.name} Carpetas")
    carpeta_alumne = carpeta_padre_out / nombre_alumne

    # Crea la nueva carpeta sino existe
    carpeta_alumne.mkdir(parents=True, exist_ok=True)
    print(f"Procesando la carpeta de {nombre_alumne}")

    # Crea la nueva dirección del archivo
    return carpeta_alumne / nombre_archivo


def main():
    """Función principal"""
    archivos = glob(input("Nombre de la carpeta: ") + r"\*.JPG")
    reduccion = float(input("Rango de reducción (0 < x < 1 ): "))

    for archivo in archivos:
        # Crea las carpetas necesarias
        direccion_destino = crear_destino(archivo)

        # Lee la imagen y la reduce
        img = cambiar_tamano(cv.imread(archivo), reduccion)

        # Guarda la imagen en la nueva dirección
        cv.imwrite(direccion_destino.as_posix(), img)
        print(f"Copiado {direccion_destino.name} reducido al {reduccion:.2%}.")

    input(f"Terminado procesado de {len(archivos)} archivos...")


if __name__ == "__main__":
    main()
