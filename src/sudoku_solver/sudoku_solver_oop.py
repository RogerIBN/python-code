"""Para mostrar la solución de un sudoku"""
from itertools import product, batched

import numpy as np


class Sudoku:
    """Clase que sostiene una partida de sudoku"""

    def __init__(self, grid: list[list[int]]) -> None:
        """
        Inicializa la rejilla del sudoku

        Parameters
        ----------
        grid : list[list[int]]
            Rejilla que almacena los números del sudoku.
        """
        self.grid = grid
        self.initial_grid = [row[:] for row in grid]

    def __repr__(self) -> str:
        return f"""\
{__class__.__name__}:(
    {np.array(self.initial_grid)}
)"""

    def __str__(self) -> str:
        sudoku_str = [
            [" ".join(str(num) for num in nums) for nums in batched(row, 3)]
            for row in self.grid
        ]
        sudoku_str = [
            "\n".join("  |  ".join(row) for row in row_quadrant)
            for row_quadrant in batched(sudoku_str, 3)
        ]
        return "\n------ + ------- + ------\n".join(sudoku_str)

    def can_set_in(self, pos_y: int, pos_x: int, num: int) -> bool:
        """
        Detecta si un numero es posible colocarlo en nuestro sudoku buscando
        coincidencias en la fila, columna y casilla.

        Parameters
        ----------
        pos_y : int
            Coordenada y
        pos_x : int
            Coordenada x
        num : int
            Numero a probar

        Returns
        -------
        bool
            La condición es posible o no.
        """
        # sourcery skip: invert-any-all, use-any, use-next
        # Revisa si no hay coincidencias en la columna
        for row in range(9):
            if self.grid[row][pos_x] == num:
                return False

        # Revisa si no hay coincidencias en la fila
        for col in range(9):
            if self.grid[pos_y][col] == num:
                return False

        # Detecta en cual de las 9 cuadrículas se encuentra la casilla
        quadrant_x = (pos_x // 3) * 3
        quadrant_y = (pos_y // 3) * 3
        # Revisa en cada casilla de la cuadrícula
        for row, col in product(range(3), repeat=2):
            if self.grid[quadrant_y + row][quadrant_x + col] == num:
                return False
        # Si ninguna condición se cumple, entonces es posible
        return True

    def solve(self) -> None:
        """
        Resuelve el sudoku probando todos los números

        Returns
        -------
        None
            Imprime la solución si devolverla.
        """
        # Itera sobre todas las casillas
        for pos_y, pos_x in product(range(9), repeat=2):
            # Si la casilla está vacía
            if self.grid[pos_y][pos_x] == 0:
                # Prueba todos los números
                for num in range(1, 10):
                    # Si es posible poner el número en la casilla
                    if self.can_set_in(pos_y, pos_x, num):
                        # Coloca ese número en el sudoku
                        self.grid[pos_y][pos_x] = num
                        # Sigue detectando
                        self.solve()
                        # Si no es posible poner el numero deshaz el intento anterior
                        # vaciando la celda
                        self.grid[pos_y][pos_x] = 0
                # Prueba otro número
                return
        print(self)
        self.save_answer("src/sudoku_solver/sudoku_solver_oop.txt")
        # Si no hay casillas vacías, terminaste con una respuesta
        # Muéstrame
        # Pausa el proceso y pregunta si quieres continuar.
        input("Continuar?")

    def save_answer(self, filename: str) -> None:
        """
        Guarda la respuesta en un archivo con el siguiente formato

        Parameters
        ----------
        filename : str
            Nombre del archivo

        6 3 9  |  4 2 5  |  7 1 8
        2 4 8  |  1 3 7  |  9 6 5
        5 7 1  |  9 6 8  |  3 4 2
        ------ + ------- + ------
        1 6 2  |  7 5 4  |  8 3 9
        4 8 3  |  6 9 2  |  5 7 1
        9 5 7  |  3 8 1  |  6 2 4
        ------ + ------- + ------
        8 2 6  |  5 4 3  |  1 9 7
        3 1 5  |  2 7 9  |  4 8 6
        7 9 4  |  8 1 6  |  2 5 3
        ========================="""
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{self}\n{'='*25}\n")


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
    sudoku.solve()


if __name__ == "__main__":
    main()
