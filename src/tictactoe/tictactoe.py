"""
Tic tac toe game
===
"""
# %%
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from command_line_interface import CommandLineInterface
from user_interface import UserInterface

BOARD_SIZE = 3
Coordinates = tuple[int, int]


class CoordinateNotInRangeError(Exception):
    """Coordinates not in range error"""

    def __init__(
        self,
        message: Optional[str] = "One or both coordinates aren't in range",
        coordinates: Optional[Coordinates] = None,
        close_open_limits: Optional[tuple[int, int]] = None,
    ) -> None:
        if coordinates:
            message = f"Coordinates{coordinates} -> {message}"
        if close_open_limits:
            min_close, max_open = close_open_limits
            message = f"{message} [{min_close}, {max_open})"

        self.coordinates = coordinates
        self.close_open_limits = close_open_limits
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


@dataclass
class Player:
    """Player class"""

    name: str
    symbol: str
    last_move: Coordinates = None, None

    def get_next_coordinates(self) -> Coordinates:
        """Get next coordinates for the player

        Returns:
            tuple(int): The next (y, x) coordinates
        """
        coordinates_str = input("Posición -> y, x: ").split(",")
        pos_y, pos_x = (int(axis) for axis in coordinates_str)
        if not (0 <= pos_y < BOARD_SIZE and 0 <= pos_x < BOARD_SIZE):
            raise CoordinateNotInRangeError(
                coordinates=(pos_y, pos_x),
                close_open_limits=(0, BOARD_SIZE),
            )

        self.last_move = pos_y, pos_x
        return self.last_move


@dataclass
class TicTacToe:
    """Tic tac toe game class"""

    user_interfase: UserInterface
    current_turn: Player
    next_turn: Player
    board: np.ndarray[str] = field(init=False)

    def __post_init__(self) -> None:
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=str)
        self.board[:] = " "

    def __str__(self) -> str:
        """Return board"""
        board = ""
        for index, row in enumerate(self.board, start=1):
            board += "  |  ".join(row)
            if index >= BOARD_SIZE:
                continue
            board += f"\n-- + {'--- + ' * (BOARD_SIZE - 2)}--\n"
        return board

    def _is_a_win(self) -> bool:
        """Check if there is a winner"""
        symbol_match = self.board == self.current_turn.symbol
        # Check rows
        if symbol_match.all(axis=1).any():
            return True
        # Check columns
        if symbol_match.all(axis=0).any():
            return True
        # Check diagonals
        if symbol_match.diagonal().all():
            return True
        if np.fliplr(symbol_match).diagonal().all():
            return True
        return False

    def _is_a_tie(self) -> bool:
        """Check if there is a tie"""
        return (self.board != " ").all()

    def _is_coordinate_available(self, coordinates: Coordinates) -> bool:
        """Check if position is valid"""
        return self.board[coordinates] == " "

    def _is_game_over(self) -> bool:
        """Check if game is over

        Returns:
            bool: True if game is over
        """
        if self._is_a_win():
            self.user_interfase.display_winner(self.current_turn.name)
            return True
        if self._is_a_tie():
            self.user_interfase.display_tie()
            return True
        return False

    def _update_board(self, coordinates: Coordinates) -> bool:
        """Updates board

        Args:
            coordinates (Coordinates): (y, x) coordinates
        """
        if not self._is_coordinate_available(coordinates):
            self.user_interfase.display_coordinate_not_available(*coordinates)
            return

        self.board[coordinates] = self.current_turn.symbol

    def _get_next_turn(self) -> None:
        """Change the turn for the next player"""
        self.current_turn, self.next_turn = self.next_turn, self.current_turn

    def start_game(self) -> None:
        """Start game"""
        while True:
            self.user_interfase.display_current_turn(
                player_name=self.current_turn.name,
                player_symbol=self.current_turn.symbol,
                board=str(self),
            )

            try:
                coordinates = self.current_turn.get_next_coordinates()
            except (ValueError, CoordinateNotInRangeError) as value_error:
                self.user_interfase.display_error(value_error)
                continue

            self._update_board(coordinates)

            if self._is_game_over():
                break

            self._get_next_turn()
        print(self)


# %%
def main():
    """Main function"""
    command_line_interface = CommandLineInterface()
    player_1 = Player("Roger", "\N{Ballot X}")
    player_2 = Player("Karla", "\N{White Circle}")
    game = TicTacToe(command_line_interface, player_1, player_2)
    game.start_game()


if __name__ == "__main__":
    main()

# %%
