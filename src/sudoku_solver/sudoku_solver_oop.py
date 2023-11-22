"""A Sudoku Solver using Object-Oriented Programming.

This module provides a Sudoku class that represents a Sudoku puzzle and
provides methods to solve the puzzle using backtracking. The Sudoku class
stores the initial grid and provides a string representation of the puzzle.

Note: The Sudoku puzzle is represented as a 9x9 grid, where 0 represents an empty cell.

For more details, please refer to the inline comments in the code.
"""
from itertools import batched, product

import numpy as np

type Grid = list[list[int]]


class Sudoku:
    """
    Class that represents a Sudoku puzzle and provides methods to solve the puzzle.
    """

    def __init__(self, grid: Grid) -> None:
        """
        Initialize a Sudoku puzzle.

        Args:
            grid (Grid): A 9x9 grid representing the Sudoku puzzle.
        """
        self.grid: Grid = grid
        self.initial_grid: Grid = [row[:] for row in grid]

    def __repr__(self) -> str:
        return f"""\
{__class__.__name__}:(
    {np.array(self.initial_grid)}
)"""

    def __str__(self) -> str:
        """String representation of the Sudoku puzzle.

        This function is a bit complicated. The general idea is that we
        split the grid into three rows, and then for each row, we split
        it into three batches of three numbers each.  Then we join each
        batch of three numbers with spaces, and then join each row with
        vertical bars, and then join each triplet of rows with horizontal
        bars. This is easier to understand visually:

        >>> print(sudoku)
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
        """
        return "\n------ + ------- + ------\n".join(
            "\n".join(
                "  |  ".join(
                    " ".join(map(str, batched_nums)) for batched_nums in batched(row, 3)
                )
                for row in batched_rows
            )
            for batched_rows in batched(self.grid, 3)
        )

    def can_set_in(self, pos_y: int, pos_x: int, num: int) -> bool:
        """
        Detects if a number can be placed in the Sudoku puzzle by checking
        for matches in the row, column, and box.

        Args:
            pos_y (int): Y coordinate
            pos_x (int): X coordinate
            num (int): Number to check
        Returns:
            bool: True if the number can be placed in the Sudoku puzzle,
            False otherwise.
        """
        # sourcery skip: invert-any-all, use-any, use-next
        # Check if there are no matches in the column
        for row in range(9):
            if self.grid[row][pos_x] == num:
                return False

        # Check if there are no matches in the row
        for col in range(9):
            if self.grid[pos_y][col] == num:
                return False

        # Check in which of the 9 boxes the cell is located
        quadrant_x = (pos_x // 3) * 3
        quadrant_y = (pos_y // 3) * 3
        # Check if there are no matches in the box
        for row, col in product(range(3), repeat=2):
            if self.grid[quadrant_y + row][quadrant_x + col] == num:
                return False
        # If no condition is met, then it is possible
        return True

    def solve(self) -> None:
        """
        Solve the Sudoku puzzle using backtracking.

        This method implements the backtracking algorithm to solve a Sudoku puzzle.
        It iterates over each cell in the grid and tries to fill it with a number
        from 1 to 9. If a number can be placed in a cell without violating the Sudoku
        rules, it is set and the algorithm continues recursively. If there are no
        possible numbers to place in a cell, the algorithm backtracks by emptying
        the cell and trying another number.

        After solving the puzzle, the method prints the solved grid and saves it to
        a text file. It also pauses the process and asks the user if they want to
        continue.
        """
        # Iter over all cells
        for pos_y, pos_x in product(range(9), repeat=2):
            # If the cell is empty
            if self.grid[pos_y][pos_x] == 0:
                # Try all numbers
                for num in range(1, 10):
                    # If it is possible to put the number in the cell
                    if self.can_set_in(pos_y, pos_x, num):
                        # Set the number in the sudoku
                        self.grid[pos_y][pos_x] = num
                        # Continue detecting
                        self.solve()
                        # If there are no ways to set the number, backtrack
                        # emptying the cell and trying another number
                        self.grid[pos_y][pos_x] = 0
                # Try another cell
                return
        # If there are no empty cells, you finished with an answer
        # Show me
        print(self)
        # Save the answer in a text file
        output_path: str = "src/sudoku_solver/sudoku_solver_oop.txt"
        self.save_answer(output_path)
        # Pause the process and ask if you want to continue.
        input("Continuar?")

    def save_answer(self, filename: str) -> None:
        """
        Save the answer of the Sudoku puzzle in a text file.

        This function appends the answer to the end of the file
        with the following format:

        >>> save_answer("sudoku_solver_oop.txt")
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
        =========================

        Args:
            filename (str): Name of the file to save the answer.
        """
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{self}\n{'='*25}\n")


def main():
    """Main program"""
    grid: Grid = [
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

    sudoku = Sudoku(grid)
    sudoku.solve()


if __name__ == "__main__":
    main()
