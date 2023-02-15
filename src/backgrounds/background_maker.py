"""Para manipular las imágenes"""
from itertools import product
from typing import Iterable

import cv2 as cv
import numpy as np

Pixel = Iterable[int]
Image = np.ndarray


def drawn_background(color: Pixel, size: Iterable[int] = (1920, 1080)) -> Image:
    """
    Crea una imagen RGB de un solo un color plano.

    Parameters
    ----------
    color : Pixel
        Color descrito en RGB
    size : Iterable[int], optional
        Tamaño de la imagen, by default (1920, 1080)

    Returns
    -------
    Image
        Imagen RGB de un color
    """
    width, height = size
    return np.full((height, width, 3), color, dtype="uint8")


def drawn_grid(img: Image, color: Pixel, gap: int = 30, thickness: int = 1) -> Image:
    """
    Dibuja una rejilla de lineas continuas en una imagen RGB

    Parameters
    ----------
    img : Image
        Imagen a dibujar
    color : Pixel
        Color descrito en RGB
    gap : int, optional
        Espacio entre lineas, by default 30
    thickness : int, optional
        Grueso de las lineas, by default 1

    Returns
    -------
    Image
        Imagen con la rejilla de lineas
    """
    height, width, _ = img.shape
    for row, column in product(range(0, height, gap), range(0, width, gap)):
        # Lineas horizontales
        cv.line(img, (0, row), (width, row), color=color, thickness=thickness)
        # Lineas verticales
        cv.line(img, (column, 0), (column, height), color=color, thickness=thickness)

    # Última linea horizontal inferior
    cv.line(
        img, (0, height - 1), (width - 1, height - 1), color=color, thickness=thickness
    )
    # Última linea vertical derecha
    cv.line(
        img, (width - 1, 0), (width - 1, height - 1), color=color, thickness=thickness
    )
    return img


def drawn_dots(img: Image, color: Pixel, gap: int = 30, radius: int = 1) -> Image:
    """
    Dibuja una rejilla de puntos en una imagen

    Parameters
    ----------
    img : Image
        Imagen a dibujar
    color : Pixel
        Color en RGB
    gap : int, optional
        Espacio entre puntos en pixeles, by default 30
    radius : int, optional
        Radio de los puntos en pixeles, by default 1

    Returns
    -------
    Image
        Imagen con la rejilla de puntos
    """
    height, width, _ = img.shape
    for row, column in product(range(gap, height, gap), range(gap, width, gap)):
        cv.circle(img, center=(column, row), radius=radius, color=color, thickness=-1)
    return img


def change_size(img: Image, rate: float) -> Image:
    """
    Cambia el tamaño de una imagen con un factor de proporción

    Parameters
    ----------
    img : Image
        Imagen a cambiar
    rate : float
        Factor de cambio de tamaño (0 < rate < 1 - reducción, rate > 1 - aumento)

    Returns
    -------
    Image
        Imagen con el tamaño cambiado
    """
    height, width, _ = img.shape
    # Redondea los nuevos tamaños a un valor entero
    width = int(width * rate)
    height = int(height * rate)
    return cv.resize(img, (width, height), interpolation=cv.INTER_AREA)


def join_images(
    foreground: Image, background: Image, coordinates: Iterable[int]
) -> Image:
    """
    Unir dos imágenes en una sola.

    Parameters
    ----------
    foreground : Image
        La imagen que se va a unir
    background : Image
        Segundo plano que se va a unir
    coordinates : Iterable[int]
        Posición de la imagen que se va a unir

    Returns
    -------
    Image
        Imagen con las figuras unidas
    """
    # Quiero colocar el logo en las coordenadas (x, y), así que
    # creo zoom_fondo_segundo_plano
    x_coord, y_coord = coordinates
    alto, ancho, _ = foreground.shape
    background_zoomed = background[y_coord : y_coord + alto, x_coord : x_coord + ancho]

    # Ahora creo una máscara del primer plano y su máscara inversa también.
    foreground_gray = cv.cvtColor(foreground, cv.COLOR_BGR2GRAY)
    _, mask = cv.threshold(foreground_gray, 10, 255, cv.THRESH_BINARY)
    # mascara = cv.erode(mascara, None)
    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # mascara = cv.morphologyEx(mascara, cv.MORPH_OPEN, kernel)
    mask_inv = cv.bitwise_not(mask)

    # Deja en negro (0, 0, 0) el area del logo en zoom_fondo_segundo_plano
    background_cropped_zoomed = cv.bitwise_and(
        background_zoomed, background_zoomed, mask=mask_inv
    )

    # Toma solo la región del logo en la imagen
    foreground_cropped = cv.bitwise_and(foreground, foreground, mask=mask)

    # Pon el logo en el zoom_fondo_segundo_plano y modifica la imagen del fondo
    joined_zoomed = cv.add(background_cropped_zoomed, foreground_cropped)
    background[y_coord : y_coord + alto, x_coord : x_coord + ancho] = joined_zoomed
    return background


def apply_vignette(img: Image, sigma: int = 200) -> Image:
    """
    Aplicar una viñeta a una imagen

    Parameters
    ----------
    img : Image
        La imagen a la que se le va a aplicar la viñeta
    sigma : int, optional
        Valor de la intensidad, by default 200

    Returns
    -------
    Image
        Imagen con la viñeta
    """
    # Calcular el alto y ancho de la imagen
    height, width, _ = img.shape

    # Genera una mascara de viñeta usando los
    # kernel gaussianos resultantes
    x_kernel = cv.getGaussianKernel(width, sigma)
    y_kernel = cv.getGaussianKernel(height, sigma)

    # Generando la matriz del kernel resultante
    kernel = y_kernel * x_kernel.T

    # Creando una máscara y normalizándose usando una
    # función de numpy
    mask = 255 * kernel / np.linalg.norm(kernel)

    # Aplicando la máscara a cada canal de la imagen
    for i in range(3):
        img[:, :, i] *= mask

    return img


def main() -> None:
    """Función principal"""
    size = (1920, 1080)
    background_color = [0] * 3
    intensity = 40
    grid_color = [intensity] * 3  # (27, 27, 27)

    background = drawn_background(background_color, size)
    # background = dibuja_puntos(background, grid_color, 30, 2)
    background = drawn_grid(background, grid_color, 30, 2)

    background = cv.cvtColor(background, cv.COLOR_RGB2BGR)
    background = cv.GaussianBlur(background, (3, 3), 0)
    # background = aplicar_viñeta(background)
    # Invertir colores del fondo
    # background = cv.bitwise_not(background)

    logo = cv.imread("src/backgrounds/images/alpha.png")
    # Cambiar tamaño de la imagen en primer plano
    logo = change_size(logo, 0.12)
    # Poner el logo en el fondo
    background = join_images(logo, background, (1830, 990))

    # Guardarla
    # cv.imwrite('src/backgrounds/images/fondo_lineas_logo.png', background)
    # cv.imwrite("src/backgrounds/images/fondo_blanco_puntos_logo.png", background)
    # cv.imwrite("src/backgrounds/images/fondo_negro_puntos_logo.png", background)
    cv.imwrite("src/backgrounds/images/fondo_negro_lineas_logo.png", background)


if __name__ == "__main__":
    main()
