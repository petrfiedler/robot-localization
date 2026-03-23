import numpy as np

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def add_tuples(a: tuple, b: tuple) -> tuple:
    """
    Add two tuples.
    :param a: First tuple.
    :param b: Second tuple.
    :return: Sum of the two tuples.
    """
    return tuple(sum(x) for x in zip(a, b))


def subtract_tuples(a: tuple, b: tuple) -> tuple:
    """
    Subtract two tuples.
    :param a: First tuple.
    :param b: Second tuple.
    :return: Difference of the two tuples.
    """
    return tuple(x - y for x, y in zip(a, b))


def rotate_matrix(matrix: np.array, clockwise=False) -> np.array:
    """
    Rotate a matrix by 90 degrees counterclockwise.
    :param matrix: Matrix to rotate.
    :param left: Rotate clockwise instead of counterclockwise.
    :return: Rotated matrix.
    """
    if clockwise:
        return np.rot90(matrix, k=3, axes=(0, 1))
    return np.rot90(matrix, k=1, axes=(0, 1))


def rotate_coords(coords: tuple[int, int], matrix_shape: tuple[int, int], n_times: int = 1, clockwise: bool = False) -> tuple[int, int]:
    """
    Rotate coordinates by 90 degrees counterclockwise n-times.
    :param coords: Coordinates to rotate.
    :param matrix_shape: Shape of the matrix.
    :param n_times: Number of times to rotate.
    :param clockwise: Rotate clockwise instead of counterclockwise.
    :return: Rotated coordinates.
    """
    for _ in range(n_times):
        if clockwise:
            coords = (coords[1], matrix_shape[0] - coords[0] - 1)
        else:
            coords = (matrix_shape[1] - coords[1] - 1, coords[0])

        matrix_shape = (matrix_shape[1], matrix_shape[0])
    return coords


def float_equal(a: float, b: float) -> bool:
    """
    Check if two floats are equal.
    :param a: First float.
    :param b: Second float.
    :return: True if the floats are equal, False otherwise.
    """
    return abs(a - b) < 1e-5


def distance(a: tuple, b: tuple, manhattan: bool = False) -> float:
    """
    Calculate the distance between two points.
    :param a: First point.
    :param b: Second point.
    :param manhattan: Use manhattan distance instead of euclidean distance.
    :return: Distance between the two points.
    """
    if manhattan:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    return np.linalg.norm(np.array(a) - np.array(b))
