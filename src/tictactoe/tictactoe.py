# %%

"""Tic tac toe game"""

from dataclasses import dataclass, field

import numpy as np

BOARD_SIZE = 3
Coordinate = tuple[int]


@dataclass
class Player:
    """Player class"""

    name: str
    symbol: str
    last_move: Coordinate = None, None
    valid_positions: set[tuple[int]] = field(
        default_factory=lambda: set(np.ndindex((BOARD_SIZE, BOARD_SIZE)))
    )

    def get_next_coordinate(self) -> Coordinate:
        """Get next coordinate for the player
        Returns:
            tuple(int): The next coordinate (y, x)
        """
        current_move = tuple(
            int(axis) for axis in input("Posición -> y, x: ").split(",")
        )

        if current_move not in self.valid_positions:
            raise ValueError(
                f"{current_move} -> y or x coordinate is not in [0, {BOARD_SIZE + 1}) range"
            )
        self.last_move = current_move
        return self.last_move


class TicTacToe:
    """Tic tac toe game class"""

    def __init__(self, current_turn: Player, next_turn: Player) -> None:
        """Initialize board"""
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=str)
        self.board[:] = " "
        self.current_turn = current_turn
        self.next_turn = next_turn

    def __str__(self) -> str:
        """Return board"""
        board = str()
        for index, row in enumerate(self.board):
            if index < (BOARD_SIZE - 1):
                board += f"{'  |  '.join(row)}\n"
                board += f"-- + {'--- + ' * (BOARD_SIZE - 2)}--\n"
            else:
                board += "  |  ".join(row)
        return board

    def _show_current_turn(self) -> None:
        """Print turn"""
        print(f"{self.current_turn.name}'s turn ({self.current_turn.symbol})")
        print(self)

    def _check_win(self) -> bool:
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

    def _check_tie(self) -> bool:
        """Check if there is a tie"""
        return (self.board != " ").all()

    def _check_valid(self, coordinate: Coordinate) -> bool:
        """Check if position is valid"""
        return self.board[coordinate] == " "

    def _game_over(self) -> bool:
        """Check if game is over

        Returns:
            bool: True if game is over
        """
        if self._check_win():
            print(f"¡Ganador: {self.current_turn.name}!")
            return True
        if self._check_tie():
            print("¡Empate!")
            return True
        return False

    def _update_board(self, coordinate: Coordinate) -> bool:
        """Return if game ended and updates board

        Args:
            coordinate (Coordinate): (y, x) coordinate

        Returns:
            bool: True if game ended
        """
        if not self._check_valid(coordinate):
            print("Posición invalida, intente nuevamente")
            return False

        self.board[coordinate] = self.current_turn.symbol

        if self._game_over():
            return True

        self.current_turn, self.next_turn = self.next_turn, self.current_turn
        return False

    def start(self) -> None:
        """Start game"""
        game_over = False
        while not game_over:
            self._show_current_turn()
            try:
                coordinate = self.current_turn.get_next_coordinate()
            except ValueError as error:
                print(error)
                continue
            game_over = self._update_board(coordinate)
        print(self)


# %%
def main():
    """Main function"""
    player_1 = Player("Roger", "\N{Ballot X}")
    player_2 = Player("Karla", "\N{White Circle}")
    game = TicTacToe(player_1, player_2)
    game.start()


if __name__ == "__main__":
    main()

# %%
