import sys
from src.parse_input import parse_input
from src.solve import solve


def handle_input(file_name: str) -> bool:
    """
    Handle input file name.
    :param file_name: Input file name.
    :return: True if input was read successfully, False otherwise.
    """

    problem = parse_input(file_name)
    if problem is None:
        return False
    solve(problem)
    return True


def ask_for_input() -> bool:
    """
    Ask user for input file name.
    :return: True if input was read successfully, False otherwise.
    """

    print("Enter input file name:")
    file_name = input()
    return handle_input(file_name)


def get_input_from_cli() -> bool:
    """
    Read input file name from command line argument.
    :return: True if input was read successfully, False otherwise.
    """

    file_name = sys.argv[1]
    return handle_input(file_name)


def read_input() -> bool:
    """
    Read and handle input from either command line or user input.
    :return: True if input was read successfully, False otherwise.
    """

    if len(sys.argv) == 1:
        return ask_for_input()

    elif len(sys.argv) == 2:
        return get_input_from_cli()

    else:
        print(f"Usage: python {sys.argv[0]} [input_file]")
        return False
