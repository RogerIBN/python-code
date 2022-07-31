import numpy as np
import cv2
from crea_fondos import *


def aplicar_vineta(imagen, sigma=200):
    # Calcular el alto y ancho de la imagen
    alto, ancho, _ = imagen.shape

    # Genera una mascara de viñeta usando los
    # kernel gaussianos resultantes
    x_kernel = cv2.getGaussianKernel(ancho, sigma * ancho / alto)
    y_kernel = cv2.getGaussianKernel(alto, sigma)

    # Generando la matriz del kernel resultante
    kernel = y_kernel * x_kernel.T

    # Creando una máscara y normalizandola usando una
    # función de numpy
    máscara = 255 * kernel / np.linalg.norm(kernel)

    # Aplicando la máscara a cada canal de la imagen
    for i in np.arange(3):
        imagen[:, :, i] = imagen[:, :, i] * máscara
    return imagen


def main():
    # Leer la imagen
    imagen = cv2.imread("fondos/images/calle.jpg")

    # Cambiar el tamaño de la imagen
    imagen = cambiar_tamano(imagen, 0.4)

    cv2.imshow("Original", imagen)

    imagen = aplicar_vineta(imagen)

    # displaying the vignette filter image
    cv2.imshow("VIGNETTE", imagen)

    # Maintain output window until
    # user presses a key
    cv2.waitKey(0)

    # Destroying present windows on screen
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
