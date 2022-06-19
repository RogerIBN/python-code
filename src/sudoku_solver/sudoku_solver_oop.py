"""Para mostrar la solución"""

from itertools import product
from numpy import array


class Sudoku:
    """Clase que sostiene una partida de sudoku"""

    def __init__(self, rejilla: list[list[int]]) -> None:
        """Inicializa la rejilla del sudoku

        Args:
            rejilla (list[list[int]]): Rejilla que almacena los números del sudoku.
        """
        self.rejilla = rejilla

    def __str__(self) -> str:
        """Método a llamar al convertir el sudoku en string.

        Returns:
            str: Representación de la partida de sudoku.
        """
        return f"{__class__.__name__}:(\n{array(self.rejilla)}\n)"

    def posible_poner(self, pos_y: int, pos_x: int, num: int) -> bool:
        """Detecta si un numero es posible colocarlo
        en nuestro sudoku buscando coincidencias en fila
        columna y casilla.
        Args:
            pos_y (int): coordenada y
            pos_x (int): coordenada x
            num (int): numero a probar
        Returns:
            bool: La condición es posible o no.
        """
        # sourcery skip: invert-any-all, use-any, use-next
        # Revisa si no hay coincidencias en la columna
        for fil in range(9):
            if self.rejilla[fil][pos_x] == num:
                return False

        # Revisa si no hay coincidencias en la fila
        for col in range(9):
            if self.rejilla[pos_y][col] == num:
                return False

        # Detecta en cual de las 9 cuadrículas se encuentra la casilla
        cuadrante_x = (pos_x // 3) * 3
        cuadrante_y = (pos_y // 3) * 3
        # Revisa en cada casilla de la cuadrícula
        for fil, col in product(range(3), range(3)):
            if self.rejilla[cuadrante_y + fil][cuadrante_x + col] == num:
                return False
        # Si ninguna condición se cumple, entonces es posible
        return True

    def resolver(self):
        """Resuelve el sudoku probando todos los números"""
        # Itera sobre todas las casillas
        for pos_y, pos_x in product(range(9), range(9)):
            # Si la casilla está vacía
            if self.rejilla[pos_y][pos_x] == 0:
                # Prueba todos los números
                for num in range(1, 10):
                    # Si es posible poner el número en la casilla
                    if self.posible_poner(pos_y, pos_x, num):
                        # Coloca ese número en el sudoku
                        self.rejilla[pos_y][pos_x] = num
                        # Sigue detectando
                        self.resolver()
                        # Si no es posible poner el numero deshaz el intento anterior
                        # vaciando la celda
                        self.rejilla[pos_y][pos_x] = 0
                # Prueba otro número
                return
        print(self)
        # Si no hay casillas vacías, terminaste con una respuesta
        # Muéstrame
        # Pausa el proceso y pregunta si quieres continuar.
        input("Continuar?")


def main():
    """Programa principal"""

    sudoku = Sudoku(
        [
            [0, 0, 0, 0, 0, 0, 7, 0, 0],
            [0, 4, 0, 0, 3, 0, 0, 6, 5],
            [0, 0, 1, 0, 0, 8, 0, 0, 0],
            [0, 6, 0, 0, 5, 0, 0, 3, 9],
            [4, 0, 0, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 0],
            [8, 0, 0, 0, 0, 3, 0, 9, 7],
            [0, 0, 0, 0, 7, 0, 4, 0, 0],
            [0, 9, 0, 0, 0, 0, 2, 0, 0],
        ]
    )
    sudoku.resolver()


if __name__ == "__main__":
    main()
