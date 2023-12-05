"""
This module contains the test cases for the `Sudoku` class in the `sudoku_solver_oop` module.
"""
import pytest

from src.sudoku_solver.sudoku_solver_oop import SudokuGame


@pytest.fixture
def sudoku() -> SudokuGame:
    """
    Fixture for the `Sudoku` class.
    """
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
    return SudokuGame(grid)


def test_solve_sudoku(sudoku: SudokuGame):  # pylint: disable=redefined-outer-name
    """
    Test case for the function `solve` in the `Sudoku` class.

    This test case verifies the correctness of the `solve` function in the `Sudoku` class.
    It checks if the puzzle is solved correctly by comparing the solved puzzle with the
    expected solution.
    """
    # before solving
    unsolved_sudoku_str = """\
Sudoku(
0 0 0  |  0 0 0  |  7 0 0
0 4 0  |  0 3 0  |  0 6 5
0 0 1  |  0 0 8  |  0 0 0
------ + ------- + ------
0 6 0  |  0 5 0  |  0 3 9
4 0 0  |  6 0 0  |  0 0 0
0 0 0  |  0 0 0  |  0 2 0
------ + ------- + ------
8 0 0  |  0 0 3  |  0 9 7
0 0 0  |  0 7 0  |  4 0 0
0 9 0  |  0 0 0  |  2 0 0
)"""

    assert str(sudoku) == unsolved_sudoku_str
    sudoku.solve()
    solved_sudoku_str = """\
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
7 9 4  |  8 1 6  |  2 5 3"""

    assert str(sudoku.results[0]) == solved_sudoku_str
