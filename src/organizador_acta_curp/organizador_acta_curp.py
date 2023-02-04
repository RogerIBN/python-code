"""Librerías para administrar directorios y
manipulación de imágenes
"""
#%%

from pathlib import Path

import cv2 as cv
import numpy as np

Mat = np.ndarray[int, np.dtype[np.generic]]


class MueveCurpActa:
    """Clase para mover archivos de una carpeta a otra"""

    def __init__(self, carpeta_origen: str):
        """Constructor de la clase.

        Args:
            carpeta_origen (str): Dirección de la carpeta de origen.
        """
        self.carpeta_origen = Path(carpeta_origen)
        self.carpeta_destino = self.carpeta_origen.with_name(
            f"{self.carpeta_origen.name} Carpetas"
        )

    @staticmethod
    def cambiar_tamano(imagen: Mat, cambio: float) -> Mat:
        """Cambia el tamaño de una imagen con
        un factor de proporción

        Args:
            imagen (Mat): Imagen a cambiar.
            cambio (float): Factor de cambio de tamaño
            0 < cambio < 1 = reducción
            cambio > 1 = aumento

        Returns:
            Mat: Imagen con el tamaño cambiado.
        """
        alto, ancho, _ = imagen.shape
        # Redondea los nuevos tamaños a un valor entero
        ancho = int(ancho * cambio)
        alto = int(alto * cambio)
        return cv.resize(imagen, (ancho, alto), interpolation=cv.INTER_AREA)

    def _crear_destino(self, archivo: Path) -> Path:
        """Crea las carpetas de destino para un archivo.

        Args:
            archivo (Path): Dirección del archivo.

        Returns:
            Path: Dirección final del archivo con su nuevo nombre.
        """
        # Extrae el nombre del alumne
        nombre_alumne = " ".join(archivo.name.split()[:-1])

        # Determina la ubicación de la carpeta del alumne
        carpeta_alumne = self.carpeta_destino / nombre_alumne

        # Crea la nueva carpeta sino existe
        if not carpeta_alumne.exists():
            print(f"Procesando la carpeta de {nombre_alumne}")
        carpeta_alumne.mkdir(parents=True, exist_ok=True)

        # Crea la nueva dirección del archivo
        return carpeta_alumne / archivo.name

    def mover_archivos(self, reduccion: float) -> None:
        """Mueve los archivos de la carpeta de origen a la carpeta de destino.

        Args:
            reduccion (float): Factor de cambio de tamaño
            0 < cambio < 1 = reducción
            cambio > 1 = aumento
        """

        contador = 0
        for contador, archivo in enumerate(self.carpeta_origen.glob("*.JPG")):
            # Crea las carpetas necesarias
            direccion_destino = self._crear_destino(archivo)

            # Lee la imagen y la reduce
            img = self.cambiar_tamano(cv.imread(str(archivo)), reduccion)

            # Guarda la imagen en la nueva dirección
            cv.imwrite(str(direccion_destino), img)
            print(f"Copiado {direccion_destino.name} reducido al {reduccion:.2%}.")
        print(f"Terminado procesado de {contador} archivos...")


def main():
    """Función principal"""
    carpeta_origen = input("Nombre de la carpeta: ")
    reduccion = float(input("Rango de reducción (0 < x < 1 ): "))
    mueve_curp_acta = MueveCurpActa(carpeta_origen)
    mueve_curp_acta.mover_archivos(reduccion)


#%%
if __name__ == "__main__":
    main()
