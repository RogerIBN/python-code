"""
Modulo para aplicar el filtro de vineta a una imagen
"""
import cv2 as cv
import background_maker as bg_maker


def main():
    """
    Función principal
    """
    # Leer la imagen
    image = cv.imread("fondos/images/calle.jpg")

    # Cambiar el tamaño de la imagen
    image = bg_maker.change_size(image, 0.4)

    cv.imshow("Original", image)

    image = bg_maker.apply_vignette(image)

    # displaying the vignette filter image
    cv.imshow("VIGNETTE", image)

    # Maintain output window until
    # user presses a key
    cv.waitKey(0)

    # Destroying present windows on screen
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
