"""
Mueve las imágenes de actas de nacimiento y CURP de una carpeta a otra de acuerdo a su
nombre y las reduce de tamaño.
"""
import logging
from pathlib import Path
from typing import Optional

import cv2 as cv
import numpy as np

Mat = np.ndarray[int, np.dtype[np.generic]]
# Crear logger---------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def change_size(img: Mat, rate: float) -> Mat:
    """
    Cambia el tamaño de una imagen con un factor de proporción

    Parameters
    ----------
    img : Mat
        Imagen a cambiar
    rate : float
        Factor de cambio de tamaño (0 < rate < 1 - reducción, rate > 1 - aumento)

    Returns
    -------
    Mat
        Imagen con el tamaño cambiado
    """
    height, width, _ = img.shape
    # Redondea los nuevos tamaños a un valor entero
    width = int(width * rate)
    height = int(height * rate)
    return cv.resize(img, (width, height), interpolation=cv.INTER_AREA)


def make_output_document_path(document: Path, output_dir: Path) -> Path:
    """
    Crea las carpetas de destino para un archivo.

    Parameters
    ----------
    document : Path
        Dirección del archivo.
    output_dir : Path
        Dirección de la carpeta de destino.

    Returns
    -------
    Path
        Dirección final del archivo con su nuevo nombre.
    """
    # Extrae el nombre del alumne
    student_name = " ".join(document.name.split()[:-1])

    # Determina la ubicación de la carpeta del alumne
    student_dir = output_dir / student_name

    # Crea la nueva carpeta sino existe
    if not student_dir.exists():
        logger.info("Procesando la carpeta de %s", student_name)
    student_dir.mkdir(parents=True, exist_ok=True)

    # Crea la nueva dirección del archivo
    return student_dir / document.name


def move_images(input_dir: Path, output_dir: Path, reduction: Optional[float]) -> None:
    """
    Mueve los archivos de la carpeta de origen a la carpeta de destino.
    Los archivos pueden ser reducidos de tamaño o aumentados.

    Parameters
    ----------
    input_dir : Path
        Carpeta de origen.
    output_dir : Path
        Carpeta de destino.
    reduction : Optional[float]
        Razón de reducción de tamaño. Si es None no se reduce el tamaño.

    See Also
    --------
    make_output_document_path : Crea las carpetas de destino para un archivo.
    bg_maker.change_size : Cambia el tamaño de una imagen.
    """
    counter = 0
    for counter, document in enumerate(input_dir.glob("*.JPG")):
        # Crea las carpetas necesarias
        output_document_path = make_output_document_path(document, output_dir)

        # Lee la imagen
        img = cv.imread(str(document))
        # Reduce el tamaño de la imagen
        if reduction:
            img = change_size(img, reduction)
            logger.debug("Reducido al %.2f%%", reduction * 100)

        # Guarda la imagen en la nueva dirección
        cv.imwrite(str(output_document_path), img)
        logger.info("Copiado %s", document.name)
    logger.info("Terminado procesado de %s archivos...", counter)


def main():
    """Función principal"""
    carpeta_origen = input("Nombre de la carpeta: ")
    reduction = float(input("Rango de reducción (0 < x < 1 ): "))
    input_dir = Path(carpeta_origen)
    output_dir = input_dir.with_name(f"{input_dir.name} Carpetas")

    move_images(input_dir, output_dir, reduction)


if __name__ == "__main__":
    main()
