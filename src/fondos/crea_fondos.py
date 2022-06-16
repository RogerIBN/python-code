"""Para manipular las imágenes"""
from itertools import product

import cv2 as cv
import numpy as np

Pixel = list[int, int, int]
Imagen = np.ndarray


def dibuja_fondo(color: Pixel, tamano: list[int, int] = (1920, 1080)) -> Imagen:
    """Crea una imagen RGB de un solo un color plano.

    Args:
        color (pixel): Color descrito en RGB.
        tamaño (list[int, int]): Tamaño de la imagen.

    Returns:
        imagen: Imagen RGB de un color.
    """
    ancho, alto = tamano
    return np.full((alto, ancho, 3), color, dtype="uint8")


def dibuja_rejilla(
    img: Imagen, color: Pixel, espaciado: int = 30, grosor: int = 1
) -> Imagen:
    """Dibuja una rejilla de lineas continuas en una imagen RGB.

    Args:
        img (imagen): Imagen a dibujar.
        color (pixel): Color descrito en RGB
        espaciado (int, optional): Espacio entre lineas en
        pixels. Defaults to 30.
        grosor (int, optional): Grueso de las lineas. Defaults to 1.

    Returns:
        imagen: imagen con la rejilla de lineas
    """
    alto, ancho, _ = img.shape
    for fila, columna in product(range(0, alto, espaciado), range(0, ancho, espaciado)):
        cv.line(img, (0, fila), (ancho, fila), color=color, thickness=grosor)
        cv.line(img, (columna, 0), (columna, alto), color=color, thickness=grosor)
    cv.line(img, (0, alto - 1), (ancho - 1, alto - 1), color=color, thickness=grosor)
    cv.line(img, (ancho - 1, 0), (ancho - 1, alto - 1), color=color, thickness=grosor)
    return img


def dibuja_puntos(
    img: Imagen, color: Pixel, espaciado: int = 30, radio: int = 1
) -> Imagen:
    """Dibuja una rejilla de puntos en una imagen

    Args:
        img (imagen): Imagen a dibujar.
        color (pixel): Color en RGB
        espaciado (int, optional): Espacio entre puntos en pixels.
        Defaults to 30.
        radio (int, optional): Radio de los puntos en pixels. Defaults to 1.

    Returns:
        imagen: Imagen con la rejilla de puntos
    """
    alto, ancho, _ = img.shape
    for fila, columna in product(
        range(espaciado, alto, espaciado), range(espaciado, ancho, espaciado)
    ):
        cv.circle(img, center=(columna, fila), radius=radio, color=color, thickness=-1)
    return img


def cambiar_tamano(img: Imagen, cambio: float) -> Imagen:
    """Cambia el tamaño de una imagen con un factor de proporción

    Args:
        imagen (imagen): Imagen a cambiar.
        cambio (float): Factor de cambio de tamaño
        0 < cambio < 1 = reducción
        cambio > 1 = aumento

    Returns:
        imagen: Imagen con el tamaño cambiado.
    """
    alto, ancho, _ = img.shape
    # Redondea los nuevos tamaños a un valor entero
    ancho = int(ancho * cambio)
    alto = int(alto * cambio)
    return cv.resize(img, (ancho, alto), interpolation=cv.INTER_AREA)


def unir_imagenes(
    primer_plano: Imagen, segundo_plano: Imagen, coordenadas: list[int, int]
) -> Imagen:
    # Quiero colocar el logo en las coordenadas (x, y), así que
    # creo zoom_fondo_segundo_plano
    x_coord, y_coord = coordenadas
    alto, ancho, _ = primer_plano.shape
    zoom_fondo_segundo_plano = segundo_plano[
        y_coord : y_coord + alto, x_coord : x_coord + ancho
    ]

    # Ahora creo una máscara del primer plano y su máscara inversa también.
    primer_plano_gris = cv.cvtColor(primer_plano, cv.COLOR_BGR2GRAY)
    _, mascara = cv.threshold(primer_plano_gris, 10, 255, cv.THRESH_BINARY)
    # máscara = cv.erode(máscara, None)
    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # máscara = cv.morphologyEx(máscara, cv.MORPH_OPEN, kernel)
    mascara_inv = cv.bitwise_not(mascara)

    # Deja en negro (0, 0, 0) el area del logo en zoom_fondo_segundo_plano
    recorte_zoom_fondo_segundo_plano = cv.bitwise_and(
        zoom_fondo_segundo_plano, zoom_fondo_segundo_plano, mask=mascara_inv
    )

    # Toma solo la región del logo en la imagen
    recorte_frente_primer_plano = cv.bitwise_and(
        primer_plano, primer_plano, mask=mascara
    )

    # Pon el logo en el zoom_fondo_segundo_plano y modifica la imagen del fondo
    zoom_primer_y_segundo_plano = cv.add(
        recorte_zoom_fondo_segundo_plano, recorte_frente_primer_plano
    )
    segundo_plano[
        y_coord : y_coord + alto, x_coord : x_coord + ancho
    ] = zoom_primer_y_segundo_plano
    return segundo_plano


def aplicar_vineta(img: Imagen, sigma: int = 200) -> Imagen:
    # Calcular el alto y ancho de la imagen
    alto, ancho, _ = img.shape

    # Genera una mascara de viñeta usando los
    # kernel gaussianos resultantes
    x_kernel = cv.getGaussianKernel(ancho, sigma)
    y_kernel = cv.getGaussianKernel(alto, sigma)

    # Generando la matriz del kernel resultante
    kernel = y_kernel * x_kernel.T

    # Creando una máscara y normalizándose usando una
    # función de numpy
    mascara = 255 * kernel / np.linalg.norm(kernel)

    # Aplicando la máscara a cada canal de la imagen
    for i in range(3):
        img[:, :, i] *= mascara

    return img


def main():
    """Función principal"""
    tamano = (1920, 1080)
    color_fondo = [0] * 3
    intensidad = 40
    color_marca = [intensidad] * 3  # (27, 27, 27)

    fondo = dibuja_fondo(color_fondo, tamano)
    fondo = dibuja_puntos(fondo, color_marca, 30, 2)
    # fondo = dibuja_rejilla(fondo, color_marca, 30, 2)

    fondo = cv.cvtColor(fondo, cv.COLOR_RGB2BGR)
    fondo = cv.GaussianBlur(fondo, (3, 3), 0)
    # fondo = aplicar_viñeta(fondo)
    # Invertir colores del fondo
    # fondo = cv.bitwise_not(fondo)

    logo = cv.imread("fondos/images/alpha.png")
    # Cambiar tamaño de la imagen en primer plano
    logo = cambiar_tamano(logo, 0.12)
    # Poner el logo en el fondo
    fondo = unir_imagenes(logo, fondo, (1830, 990))

    # Guardarla
    # cv.imwrite('fondos/images/fondo_lineas_logo.png', fondo)
    # cv.imwrite("fondos/images/fondo_blanco_puntos_logo.png", fondo)
    cv.imwrite("fondos/images/fondo_negro_puntos_logo.png", fondo)


if __name__ == "__main__":
    main()