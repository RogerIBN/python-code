"""
A solution to the FizzBuzz problem.
"""
from itertools import compress

Divisor = int
Word = str
Rules = dict[Divisor, Word]


def main():
    """
    The main function.
    """

    rules: Rules = {
        2: "Fizz",
        5: "Buzz",
        7: "Bazz",
    }

    limit = 15

    game_logic(rules, limit)


def game_logic(rules: Rules, limit: int) -> None:
    """
    A function that prints the numbers from 1 to limit according to the rules
    of the game.

    Args:
        rules (dict[int, str]): A dictionary containing the rules of the game.
        The keys are the divisors and the values are the strings to be printed
        when the number is divisible by the key.
        limit (int): An integer representing the limit of the game.
    """
    for number in range(1, limit + 1):
        final_string = "".join(
            word for divisor, word in rules.items() if number % divisor == 0
        ) or str(number)
        print(final_string)


if __name__ == "__main__":
    main()
