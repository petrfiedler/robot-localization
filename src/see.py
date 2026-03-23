from queue import Queue
import numpy as np
import math

from src.problem import Problem
from src.config import *
from src.constants import *
from src.helpers import add_tuples, subtract_tuples, DIRECTIONS


def get_corners(block: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Get the corners of a block.
    :param block: Block.
    :return: Corners.
    """

    relative_corners = [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)]
    corners = [add_tuples(block, delta) for delta in relative_corners]
    return corners


def get_angle(outer: tuple[int, int], inner: tuple[int, int]) -> float:
    """
    Get the angle relative to (1, 0) of outer vector centered by inner vector.
    :param inner: Inner vector.
    :param outer: Outer vector.
    :return: Angle in radians.
    """

    zero_angle_vector = np.array([1, 0])
    inner_vector = np.array(inner)
    outer_vector = np.array(outer)

    centered_vector = outer_vector - inner_vector
    angle = np.arccos(
        np.dot(zero_angle_vector, centered_vector) /
        np.linalg.norm(centered_vector)
    )

    # modify the angle if the vector is in the 3rd or 4th quadrant
    if inner_vector[1] > outer_vector[1]:
        angle = 2 * math.pi - angle

    return angle


def outer_angles(angles: list[float]) -> tuple[float, float]:
    """
    Get the most distant angles from the given list, assuming all the angles are acute.
    :param angles: List of angles.
    :return: Tuple containing the most distant angles.
    """

    # special case: there is angle both < pi/2 and > 3pi/2
    if min(angles) < math.pi / 2 and max(angles) > 3 * math.pi / 2:
        less_than_pi_2 = [angle for angle in angles if angle < math.pi / 2]
        more_than_3pi_2 = [
            angle for angle in angles if angle > 3 * math.pi / 2]
        return max(less_than_pi_2), min(more_than_3pi_2)

    return max(angles), min(angles)


def region_contains_angle(region: tuple[float, float], angle: float) -> bool:
    """
    Check if the given angle is contained in the given region.
    :param region: Region - tuple of two angles.
    :param angle: Angle.
    """

    if region[0] < region[1]:
        return region[0] >= angle or region[1] <= angle

    return region[0] >= angle and region[1] <= angle


def subtract_angle_regions(eater: tuple[float, float], food: tuple[float, float]) -> tuple[float, float]:
    """
    Given two angle regions, subtract the intersection of the regions from the food.
    :param eater: Eater region.
    :param food: Food region.
    :return: Modified food region.
    """

    if region_contains_angle(eater, food[0]) and region_contains_angle(eater, food[1]):
        return None

    elif region_contains_angle(food, eater[0]):
        # eater must be bigger than food
        if region_contains_angle(food, eater[1]):
            return food
        return (food[0], eater[0])

    elif region_contains_angle(food, eater[1]):
        return (eater[1], food[1])

    return food


def shadow_is_cast(block: tuple[int, int], source: tuple[int, int], walls_seen: set[tuple[int, int]]) -> bool:
    """
    Check if the walls seen cast a shadow on the block from the source.
    :param block: Block.
    :param source: Source.
    :param walls_seen: Walls seen.
    :return: True if shadow is cast, False otherwise.
    """

    block_corners = get_corners(block)
    block_corner_angles = [get_angle(corner, source)
                           for corner in block_corners]
    block_outer_angles = outer_angles(block_corner_angles)

    visible_part = block_outer_angles

    for wall in walls_seen:
        wall_corners = get_corners(wall)
        wall_angles = [get_angle(corner, source) for corner in wall_corners]
        wall_outer_angles = outer_angles(wall_angles)

        visible_part = subtract_angle_regions(wall_outer_angles, visible_part)
        if visible_part is None:
            return True

    return False


def see(problem: Problem) -> None:
    """
    Let the robot see the environment around him.
    :param problem: Problem.
    """

    start = problem.current_position()
    problem.seen_halls.add(start)

    q = Queue()
    q.put(start)
    visited = {start}
    walls_seen = set()

    while not q.empty():
        current = q.get()
        problem.seen[current] = True

        relative_position = subtract_tuples(current, problem.start)
        kernel_position = add_tuples(
            problem.kernel_center(), relative_position)
        kernel_value = WALL if problem.map[current] == WALL else EMPTY
        problem.kernel[kernel_position] = kernel_value

        # if neighbor is wall, don't check for it's neighbors
        if problem.map[current] == WALL:
            continue

        for direction in DIRECTIONS:
            neighbor = tuple(sum(x) for x in zip(current, direction))

            if neighbor in visited:
                continue

            # don't look around corners
            if shadow_is_cast(neighbor, start, walls_seen):
                continue

            # check if neighbor is in visible distance
            if round(np.linalg.norm(np.array(start) - np.array(neighbor))) > VISIBILITY_DISTANCE:
                continue

            q.put(neighbor)
            visited.add(neighbor)

            if problem.map[neighbor] == WALL:
                walls_seen.add(neighbor)

            else:
                problem.seen_halls.add(neighbor)

    problem.walls_to_see = problem.walls_to_see - walls_seen
