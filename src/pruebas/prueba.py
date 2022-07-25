"""Game script"""


def is_int(user_number: str) -> bool:
    """Checks if the user input is an integer

    Args:
        user_number (Any): User input

    Returns:
        bool: If the user input is an integer
    """
    try:
        int(user_number)
        return True
    except ValueError:
        print("Enter a whole number only")
        return False


input_ok: bool = False

while not input_ok:
    menu_number_input = input("Please select from 1 through: ")
    input_ok: bool = is_int(menu_number_input)

menu_number_input = int(menu_number_input)
