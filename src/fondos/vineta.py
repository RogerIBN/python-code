import cv2 as cv
from crea_fondos import *


def main():
    # Leer la imagen
    image = cv.imread("fondos/images/calle.jpg")

    # Cambiar el tamaño de la imagen
    image = change_size(image, 0.4)

    cv.imshow("Original", image)

    image = apply_vignette(image)

    # displaying the vignette filter image
    cv.imshow("VIGNETTE", image)

    # Maintain output window until
    # user presses a key
    cv.waitKey(0)

    # Destroying present windows on screen
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
