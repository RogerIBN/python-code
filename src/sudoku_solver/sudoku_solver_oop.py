"""A Sudoku Solver using Object-Oriented Programming.

This module provides a Sudoku class that represents a Sudoku puzzle and
provides methods to solve the puzzle using backtracking. The Sudoku class
stores the initial grid and provides a string representation of the puzzle.

Note: The Sudoku puzzle is represented as a 9x9 grid, where 0 represents an empty cell.

For more details, please refer to the inline comments in the code.
"""
# %%
from collections import UserList
from itertools import chain
from typing import Any, Sequence, SupportsIndex, overload


class SudokuGrid(UserList[list[int]]):
    """
    A 9x9 grid representing the Sudoku puzzle.
    """

    drawn_grid: str = """\
0 0 0  |  0 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 0 0
------ + ------- + ------
0 0 0  |  0 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 0 0
------ + ------- + ------
0 0 0  |  0 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 0 0""".replace(
        "0", "{}"
    )

    def __init__(self, grid: Sequence[list[int]]) -> None:
        if not self._is_valid_grid(grid):
            raise ValueError("Invalid grid")
        super().__init__(grid)

    def __repr__(self) -> str:
        return f"""{self.__class__.__name__}(
{'\n'.join(repr(row) for row in self.data)}
)"""

    def __str__(self) -> str:
        """
        String representation of the Sudoku puzzle.

        Consists of a 9x9 grid, where each cell is represented by a number.
        Empty cells are represented by 0.

        Example:
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
        return self.drawn_grid.format(*chain.from_iterable(self))

    @overload
    def __getitem__(self, index: slice) -> list[list[int]]:
        ...

    @overload
    def __getitem__(self, index: SupportsIndex) -> list[int]:
        ...

    @overload
    def __getitem__(self, index: tuple[SupportsIndex, SupportsIndex]) -> int:
        ...

    def __getitem__(self, index):
        match index:
            case index if isinstance(index, SupportsIndex):
                return self.data[index]
            case y, x if all(isinstance(index, int) for index in index):
                return self.data[y][x]
            case _:
                raise TypeError("Invalid key type")

    def __setitem__(
        self, key: tuple[SupportsIndex, SupportsIndex] | int | slice, value: Any
    ) -> None:
        match key:
            case y, x if all(isinstance(index, int) for index in key):
                if value != 0 and not self.can_set_in(y, x, value):  # type: ignore
                    raise ValueError(f"Value {value} cannot be set")
                self.data[y][x] = value
            case y, x if any(isinstance(index, slice) for index in key):
                raise TypeError("Set an item using slicing is not supported")
            case _:
                raise TypeError("Invalid key type")

    def _is_valid_grid(self, grid: Sequence[Sequence[Any]]) -> bool:
        if len(grid) != 9:
            return False
        if any(len(row) != 9 for row in grid):
            return False
        return all(self._is_valid_value(value) for row in grid for value in row)

    def _is_valid_value(self, value: Any) -> bool:
        num = int(value)
        return 0 <= num <= 9

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
        # Check if there are no matches in the row
        if num in self.data[pos_y]:
            return False

        # Check if there are no matches in the column
        for row in self.data:
            if row[pos_x] == num:
                return False

        # Check in which of the 9 boxes the cell is located
        quadrant_y = (pos_y // 3) * 3
        quadrant_x = (pos_x // 3) * 3
        # Check if there are no matches in the box
        for row in self.data[quadrant_y : quadrant_y + 3]:
            if num in row[quadrant_x : quadrant_x + 3]:
                return False
        # If no condition is met, then it is possible
        return True

    def copy(self):
        return self.__class__([row[:] for row in self.data])


class SudokuGame:
    """
    Class that represents a Sudoku puzzle and provides methods to solve the puzzle.

    Attributes:
        grid (Grid): A 9x9 grid representing the Sudoku puzzle.
        initial_grid (Grid): A copy of the initial grid.
    """

    def __init__(self, grid) -> None:
        """
        Initialize a Sudoku puzzle.

        Args:
            grid (Grid): A 9x9 grid representing the Sudoku puzzle.
        """
        self.grid: SudokuGrid = SudokuGrid(grid)
        self.results: list[SudokuGrid] = []

    def __repr__(self) -> str:
        return f"""\
{__class__.__name__}(
{self.grid!r}
)"""

    def __str__(self) -> str:
        """
        String representation of the Sudoku puzzle.

        Consists of a 9x9 grid, where each cell is represented by a number.
        Empty cells are represented by 0.

        Example:
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
        return f"""\
{self.__class__.__name__}(
{self.grid}
)"""

    def solve(self):
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
        for pos_y, row in enumerate(self.grid):
            for pos_x, cell in enumerate(row):
                # If the cell is empty
                if cell == 0:
                    # Try all numbers
                    for num in range(1, 10):
                        if self.grid.can_set_in(pos_y, pos_x, num):
                            # Set the number in the sudoku
                            row[pos_x] = num
                            # Continue detecting
                            self.solve()
                            # If there are no ways to set the number, backtrack
                            # emptying the cell and trying another number
                            row[pos_x] = 0
                    # Try another cell
                    return
        # If there are no empty cells, you finished with an answer
        self.results.append(self.grid.copy())

    def save_results(self, filename: str) -> None:
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

        Raises:
            ValueError: If there are no results to save.
        """
        if not self.results:
            self.solve()

        with open(filename, "r", encoding="utf-8") as file:
            text = f"\n{'='*25}\n".join(str(result) for result in self.results)
            file.write(text)


# %%


def main():
    """Main program"""
    # %%
    grid = [
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
    # %%

    sudoku = SudokuGame(grid)
    print(sudoku)
    sudoku.solve()
    sudoku.save_results("src/sudoku_solver/sudoku_solver_oop.txt")


# %%
if __name__ == "__main__":
    main()
