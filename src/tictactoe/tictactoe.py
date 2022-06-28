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
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return True
        # Check columns
        for col in range(3):
            if self.board[0, col] == self.board[1, col] == self.board[2, col] != " ":
                return True
        # Check diagonals
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != " ":
            return True
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != " ":
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

    def update_board(self, pos_y: int, pos_x: int) -> None:
        """Update board"""
        if self.check_valid(pos_y, pos_x):
            self.board[pos_y, pos_x] = self.current_turn.symbol
            self.current_turn, self.next_turn = self.next_turn, self.current_turn
        else:
            print("Posición invalida")

    def start(self) -> None:
        """Start game"""
        while True:
            if self.check_win():
                print(f"Ganador: {self.next_turn.name}")
                break
            if self.check_tie():
                print("Empate")
                break

            self.print_turn()

            pos_y, pos_x = int(input("Posición y: ")), int(input("Posición x: "))
            self.update_board(pos_y, pos_x)
        print(self)


def main():
    """Main function"""
    player_1 = Player("Roger", "X")
    player_2 = Player("Karla", "O")
    game = TicTacToe(player_1, player_2)
    game.start()


if __name__ == "__main__":
    main()
