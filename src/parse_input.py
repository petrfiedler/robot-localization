import numpy as np
import re

from src.problem import Problem
from src.constants import *


def read_input_file(file_name: str) -> str:
    """
    Read input file.
    :param file_name: Input file name.
    :return: Input file contents if file was read successfully, None otherwise.
    """

    try:
        with open(file_name, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None


def check_problem_validity(problem: Problem) -> bool:
    """
    Check problem validity.
    :param problem: Problem instance.
    :return: True if problem is valid, False otherwise.
    """

    # check if map is at least 3x3 (one empty surrounded by walls)
    if problem.map.shape[0] < 3 or problem.map.shape[1] < 3:
        print("Map is too small.")
        return False

    # check if map has a border
    if np.sum(problem.map[0, :]) != problem.map.shape[1] or \
       np.sum(problem.map[-1, :]) != problem.map.shape[1] or \
       np.sum(problem.map[:, 0]) != problem.map.shape[0] or \
       np.sum(problem.map[:, -1]) != problem.map.shape[0]:
        print("Map does not have a border.")
        return False

    # check that start is in the map
    if not problem.is_in_map(problem.start):
        print("Start is not in the map.")
        return False

    # check that start is not an obstacle
    if problem.is_obstacle(problem.start):
        print("Start is an obstacle.")
        return False

    return True


def parse_input(file_name: str) -> Problem:
    """
    Parse input file.
    :param file_name: Input file name.
    :return: Problem instance if input was read successfully, None otherwise.
    """

    input_str = read_input_file(file_name)
    if input_str is None:
        return None

    # split input file into lines
    lines = input_str.rstrip().splitlines()

    # minimum: wall + empty + wall + start
    if len(lines) < 4:
        print("Invalid input file.")
        return None

    # parse map
    map_grid = np.array([list(line) for line in lines[:-1]])

    # replace X by 1 and spaces by 0
    map_grid = np.where(map_grid == 'X', WALL, EMPTY)

    # parse start
    pattern = r"(\d+),\s*(\d+)"
    match = re.search(pattern, lines[-1])
    if match:
        start = (int(match.group(1)), int(match.group(2)))
    else:
        return None

    problem = Problem(map_grid, start)

    if not check_problem_validity(problem):
        return None

    return problem
