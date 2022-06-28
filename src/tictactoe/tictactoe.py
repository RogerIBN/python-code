# %%

"""Tic tac toe game"""

from dataclasses import dataclass
import numpy as np


@dataclass
class Player:
    """Player class"""

    name: str
    symbol: str


class TicTacToe:
    """Tic tac toe game class"""

    def __init__(self, player_1: Player, player_2: Player) -> None:
        """Initialize board"""
        self.board = np.zeros((3, 3), dtype=str)
        self.board[:] = " "
        self.current_turn = player_1
        self.next_turn = player_2

    def print_turn(self) -> None:
        """Print turn"""
        print(f"{self.current_turn.name}'s turn ({self.current_turn.symbol})")
        print(self)

    def __str__(self) -> str:
        """Return board"""
        return f"{self.board[0]}\n{self.board[1]}\n{self.board[2]}"

    def check_win(self) -> bool:
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

    def check_tie(self) -> bool:
        """Check if there is a tie"""
        return all(" " not in row for row in self.board)

    def check_valid(self, pos_y: int, pos_x: int) -> bool:
        """Check if position is valid"""
        return (pos_y in range(3) and pos_x in range(3)) and self.board[
            pos_y, pos_x
        ] == " "

    def update_board(self, pos_y: int, pos_x: int) -> bool:
        """Return if game ended and updates board

        Args:
            pos_y (int): Y coordinate
            pos_x (int): X coordinate

        Returns:
            bool: True if game ended
        """
        if not self.check_valid(pos_y, pos_x):
            print("Posición invalida")
            return False

        self.board[pos_y, pos_x] = self.current_turn.symbol

        if self.check_win():
            print(f"¡Ganador: {self.current_turn.name}!")
            return True
        if self.check_tie():
            print("¡Empate!")
            return True
        self.current_turn, self.next_turn = self.next_turn, self.current_turn
        return False

    def start(self) -> None:
        """Start game"""
        game_ended = False
        while not game_ended:
            self.print_turn()
            pos_y, pos_x = int(input("Posición y: ")), int(input("Posición x: "))
            game_ended = self.update_board(pos_y, pos_x)
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
