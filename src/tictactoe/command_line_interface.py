"""Command line interface for TicTacToe"""


class CommandLineInterface:
    """User Interface Protocol"""

    @staticmethod
    def display_error(error: Exception) -> None:
        """Display error message"

        Args:
            error (Exception): Error message
        """
        print(f"{error}. Please, try again...")

    @staticmethod
    def display_current_turn(player_name: str, player_symbol: str, board: str) -> None:
        """Display current turn message

        Args:
            player_name (str): Current turn player name
            player_symbol (str): Current turn player symbol
            board (str): Board string
        """
        print(f"{player_name}'s turn ({player_symbol})")
        print(board)

    @staticmethod
    def display_winner(winner_name: str) -> None:
        """Display winner message

        Args:
            winner_name (str): The name of the winner
        """
        print(f"You won {winner_name}!")

    @staticmethod
    def display_tie() -> None:
        """Display tie message"""
        print("It's a tie!")

    @staticmethod
    def get_next_coordinates() -> tuple[int, int]:
        """Get next coordinate

        Returns:
            tuple[int, int]: The next coordinate
        """
        coordinates_str = input("Position -> y, x: ").split(",")
        return tuple(int(axis) for axis in coordinates_str)
