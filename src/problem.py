import numpy as np
from copy import deepcopy

from src.constants import *
from src.helpers import add_tuples


class Problem:
    """
    Class containing the problem to be solved.
    """

    def __init__(self, map: np.ndarray, start: tuple) -> None:
        """
        Constructor.
        :param map: Map.
        :param start: Start position.
        """

        # array containing the map (0: free, 1: obstacle)
        self.map = map

        # start position (row, col)
        self.start = start

        # relative position to start(row, col)
        self.relative_position = (0, 0)

        # current direction (row, col)
        self.direction = None

        # visited positions
        self.visited = np.zeros_like(self.map, dtype=bool)

        # kernel depicting scanned environment, starting position in the middle
        self.kernel_size = 2 * \
            (max(self.map.shape[0], self.map.shape[1]) - 1) + 1
        self.kernel = np.zeros(
            (self.kernel_size, self.kernel_size), dtype=int)

        # array containing possible starting points
        self.possible_starts = np.zeros_like(self.map, dtype=bool)

        # array containing seen pixels
        self.seen = np.zeros_like(self.map, dtype=bool)

        # set of all seen halls
        self.seen_halls = set()

        # set of all walls that can yet to be seen
        self.walls_to_see = set()

        # target to head to
        self.target = None

        # path to target
        self.path_to_target = None

        # entropy of unseen blocks in kernel
        self.entropy = np.array(self.kernel, dtype=float)

        # set of coordinates with max entropy
        self.max_entropy = set()

    def is_in_map(self, position: tuple) -> bool:
        """
        Check if position is in the map.
        :param position: Position to check.
        :return: True if position is in the map, False otherwise.
        """
        return (0 <= position[0] < self.map.shape[0]) and \
               (0 <= position[1] < self.map.shape[1])

    def is_obstacle(self, position: tuple) -> bool:
        """
        Check if position is an obstacle.
        :param position: Position to check.
        :return: True if position is an obstacle, False otherwise.
        """
        return self.map[position[0], position[1]] == WALL

    def kernel_center(self) -> tuple[int, int]:
        """
        Return the middle of the kernel.
        :return: Middle of the kernel.
        """
        return (self.kernel_size // 2, self.kernel_size // 2)

    def current_position(self) -> tuple[int, int]:
        """
        Return the current position.
        :return: Current position.
        """
        return add_tuples(self.start, self.relative_position)

    def move(self, direction: tuple[int, int]) -> None:
        """
        Walk in a direction.
        :param direction: Direction to walk.
        """
        self.relative_position = add_tuples(self.relative_position, direction)

    def number_of_possibles(self) -> int:
        """
        Return the number of possible starting points.
        :return: Number of possible starting points.
        """
        return np.sum(self.possible_starts)

    def deep_copy(self):
        return deepcopy(self)
