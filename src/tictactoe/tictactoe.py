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
type Coordinates = tuple[int, int]


class CoordinateNotInRangeError(ValueError):
    """Coordinates not in range error"""

    def __init__(
        self,
        message: str = "One or both coordinates aren't in range",
        coordinates: Optional[Coordinates] = None,
        close_open_limits: Optional[Coordinates] = None,
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
    _last_move: Coordinates = -1, -1

    @property
    def last_move(self) -> Coordinates:
        """Last move property"""
        return self._last_move

    @last_move.setter
    def last_move(self, coordinates: Coordinates) -> None:
        """Last move setter of coordinates"""
        if any(
            coordinate < 0 or coordinate >= BOARD_SIZE for coordinate in coordinates
        ):
            raise CoordinateNotInRangeError(
                coordinates=coordinates,
                close_open_limits=(0, BOARD_SIZE),
            )

        self._last_move = coordinates


@dataclass
class TicTacToe:
    """Tic tac toe game class"""

    user_interfase: UserInterface
    current_player: Player
    next_player: Player
    board: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=str)
        self.board[:] = " "

    def __str__(self) -> str:
        """Return board"""
        return f"\n-- + {'--- + ' * (BOARD_SIZE - 2)}--\n".join(
            "  |  ".join(row) for row in self.board
        )

    def _is_a_win(self) -> bool:
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, reintroduce-else
        """Check if there is a winner"""
        symbol_match = self.board == self.current_player.symbol
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
            self.user_interfase.display_winner(self.current_player.name)
            return True
        if self._is_a_tie():
            self.user_interfase.display_tie()
            return True
        return False

    def _update_board(self, coordinates: Coordinates) -> None:
        """Updates board

        Args:
            coordinates (Coordinates): (y, x) coordinates
        """
        if not self._is_coordinate_available(coordinates):
            raise ValueError(f"Box {coordinates} already taken")
        self.board[coordinates] = self.current_player.symbol

    def _get_next_turn(self) -> None:
        """Change the turn for the next player"""
        self.current_player, self.next_player = self.next_player, self.current_player

    def start_game(self) -> None:
        """Start game"""
        while True:
            self.user_interfase.display_current_turn(
                player_name=self.current_player.name,
                player_symbol=self.current_player.symbol,
                board=str(self),
            )

            try:
                coordinates = self.user_interfase.get_next_coordinates()
                if len(coordinates) != 2:
                    raise ValueError("Coordinates must be a tuple of length 2")
                self.current_player.last_move = coordinates
                self._update_board(coordinates)
            except ValueError as error:
                self.user_interfase.display_error(error)
                continue

            if self._is_game_over():
                break

            self._get_next_turn()
        print(self)


# %%
def main() -> None:
    """Main function"""
    command_line_interface = CommandLineInterface()
    player_1 = Player("Roger", "\N{Ballot X}")
    player_2 = Player("Karla", "\N{White Circle}")
    game = TicTacToe(command_line_interface, player_1, player_2)
    game.start_game()


if __name__ == "__main__":
    main()

# %%
