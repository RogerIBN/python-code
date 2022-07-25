"""User interface for TicTacToe."""
from typing import Protocol


class UserInterface(Protocol):
    """User Interface Protocol"""

    def display_error(self, error: Exception) -> None:
        """Display error message"

        Args:
            error (Exception): Error message
        """
        raise NotImplementedError()

    def display_current_turn(
        self, player_name: str, player_symbol: str, board: str
    ) -> None:
        """Display current turn message

        Args:
            player_name (str): Current turn player name
            player_symbol (str): Current turn player symbol
            board (str): Board string
        """
        raise NotImplementedError()

    def display_winner(self, winner_name: str) -> None:
        """Display winner message

        Args:
            winner_name (str): The name of the winner
        """
        raise NotImplementedError()

    def display_tie(self) -> None:
        """Display tie message"""
        raise NotImplementedError()

    def get_next_coordinates(self) -> tuple[int, int]:
        """Get next coordinate

        Returns:
            tuple[int, int]: The next coordinate
        """
        raise NotImplementedError()
