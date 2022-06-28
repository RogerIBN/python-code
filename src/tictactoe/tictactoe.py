# %%

"""Tic tac toe game"""

from dataclasses import dataclass
import numpy as np


@dataclass
class Player:
    """Player class"""

    name: str
    symbol: str
    last_move: tuple[int] = None, None

    def get_next_coordinate(self) -> tuple[int]:
        """Get next coordinate for the player
        Returns:
            tuple(int): The next coordinate (y, x)
        """
        current_move = int(input("Posición y: ")), int(input("Posición x: "))
        self.last_move = current_move
        return self.last_move


class TicTacToe:
    """Tic tac toe game class"""

    valid_positions = {(pos_y, pos_x) for pos_y in range(3) for pos_x in range(3)}

    def __init__(self, player_1: Player, player_2: Player) -> None:
        """Initialize board"""
        self.board = np.zeros((3, 3), dtype=str)
        self.board[:] = " "
        self.current_turn = player_1
        self.next_turn = player_2

    def _print_turn(self) -> None:
        """Print turn"""
        print(f"{self.current_turn.name}'s turn ({self.current_turn.symbol})")
        print(self)

    def __str__(self) -> str:
        """Return board"""
        return f"{self.board[0]}\n{self.board[1]}\n{self.board[2]}"

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

    def _check_valid(self, coordinate: tuple[int]) -> bool:
        """Check if position is valid"""
        return coordinate in self.valid_positions and self.board[coordinate] == " "

    def _update_board(self, coordinate: tuple[int]) -> bool:
        """Return if game ended and updates board

        Args:
            coordinate (tuple[int]): (y, x) coordinate

        Returns:
            bool: True if game ended
        """
        if not self._check_valid(coordinate):
            print("Posición invalida, intente nuevamente")
            return False

        self.board[coordinate] = self.current_turn.symbol

        if self._check_win():
            print(f"¡Ganador: {self.current_turn.name}!")
            return True
        if self._check_tie():
            print("¡Empate!")
            return True
        self.current_turn, self.next_turn = self.next_turn, self.current_turn
        return False

    def start(self) -> None:
        """Start game"""
        game_ended = False
        while not game_ended:
            self._print_turn()
            coordinate = self.current_turn.get_next_coordinate()
            game_ended = self._update_board(coordinate)
        print(self)


# %%
def main():
    """Main function"""
    player_1 = Player("Roger", "X")
    player_2 = Player("Karla", "O")
    game = TicTacToe(player_1, player_2)
    game.start()


if __name__ == "__main__":
    main()

# %%
