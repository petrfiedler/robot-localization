import numpy as np
from scipy.signal import fftconvolve
from queue import Queue, PriorityQueue
from collections import deque
import random

from src.problem import Problem
from src.show import Display
from src.see import see
from src.helpers import rotate_matrix, float_equal, add_tuples, subtract_tuples, DIRECTIONS, distance, rotate_coords
from src.constants import *


def get_edge_halls(problem: Problem) -> list[tuple[int, int]]:
    """
    Get the halls in kernel that has at least one unseen neighbour.
    :param problem: Problem.
    :return: Halls on the edge of the kernel.
    """

    edge_halls = set()
    for hall in problem.seen_halls:
        hall_relative = subtract_tuples(hall, problem.start)
        for direction in DIRECTIONS:
            kernel_hall = add_tuples(problem.kernel_center(), hall_relative)
            neighbour = add_tuples(kernel_hall, direction)
            if problem.kernel[neighbour] == 0:
                edge_halls.add(kernel_hall)
                break

    return edge_halls


def get_max_entropy(problem: Problem) -> set[tuple[int, int]]:
    """
    Get cells with maximum non-zero entropy.
    :param problem: Problem.
    """
    
    max_entropy = np.amax(problem.entropy)
    if max_entropy == 0:
        problem.max_entropy = set()
        return
    problem.max_entropy = np.argwhere(problem.entropy == max_entropy)


def get_real_distance(problem: Problem, start: tuple[int, int], end: tuple[int, int]) -> int:
    """
    Get real distance between two points in kernel.
    :param problem: Problem.
    :param start: Start point.
    :param end: End point.
    :return: Real distance.
    """

    q = PriorityQueue()
    q.put((0, start))
    seen = set()
    seen.add(start)
    distances = {start: 0}

    while not q.empty():
        current = q.get()[1]

        if current == end:
            return distances[current]

        for direction in DIRECTIONS:
            next = add_tuples(current, direction)

            if next in seen or problem.kernel[next] != EMPTY:
                continue

            seen.add(next)
            distance_to_end = distance(next, end)
            distances[next] = distances[current] + 1
            q.put((distances[next] + distance_to_end, next))


def get_target(problem: Problem) -> None:
    """
    Get the target to head to.
    :param problem: Problem.
    """

    edge_halls = get_edge_halls(problem)

    # get edge hall that is the closest to some element of max_entropy
    min_distance = float('inf')
    for hall in edge_halls:
        for max_entropy in problem.max_entropy:
            kernel_current = add_tuples(
                problem.kernel_center(), problem.relative_position)
            dist = distance(hall, max_entropy, manhattan=True) + \
                get_real_distance(problem, kernel_current, hall)
            if dist < min_distance:
                min_distance = dist
                problem.target = add_tuples(
                    problem.start, subtract_tuples(hall, problem.kernel_center()))


def reconstruct_path(previous: dict[tuple[int, int], tuple[int, int]], target: tuple[int, int]) -> deque[tuple[int, int]]:
    """
    Reconstruct the path.
    :param previous: Previous.
    :param target: Target.
    :return: Path.
    """

    path = deque()
    current = target

    while current:
        path.appendleft(current)
        current = previous[current]

    return path


def get_path_to_target(problem: Problem) -> None:
    """
    Get the path to the target.
    :param problem: Problem.
    """
    # A star
    q = PriorityQueue()
    q.put((0, problem.current_position()))
    seen = set()
    seen.add(problem.current_position())
    previous = {problem.current_position(): None}
    distances = {problem.current_position(): 0}

    while not q.empty():
        current = q.get()[1]

        if current == problem.target:
            break

        for direction in DIRECTIONS:
            next = add_tuples(current, direction)
            next_relative = subtract_tuples(next, problem.start)
            kernel_next = add_tuples(problem.kernel_center(), next_relative)

            if next in seen or problem.kernel[kernel_next] != EMPTY:
                continue

            seen.add(next)
            previous[next] = current
            distances[next] = distances[current] + 1
            q.put((distances[next] + distance(next, problem.target), next))

    problem.path_to_target = reconstruct_path(previous, problem.target)


def get_the_best_direction(problem: Problem) -> None:
    """
    Get the best direction to go.
    :param problem: Problem.
    """

    old_target = problem.target
    get_target(problem)

    if old_target != problem.target:
        get_path_to_target(problem)

    if not problem.path_to_target:
        halls = set()
        for direction in DIRECTIONS:
            next = add_tuples(problem.current_position(), direction)
            if problem.is_in_map(next) and problem.map[next] == EMPTY:
                halls.add(next)
        problem.target = random.choice(list(halls))
        return

    next_block = problem.path_to_target.popleft()
    problem.direction = subtract_tuples(next_block, problem.current_position())


def find_walls_to_see(problem: Problem) -> None:
    """
    Find all walls that can be seen.
    :param problem: Problem.
    """

    q = Queue()
    q.put(problem.start)
    problem.walls_to_see = set()
    visited = set()

    while not q.empty():
        current = q.get()
        for d in DIRECTIONS:
            next = add_tuples(current, d)

            if not problem.is_in_map(next) or next in visited:
                continue

            visited.add(next)

            if problem.map[next] == WALL:
                problem.walls_to_see.add(next)
            else:
                q.put(next)


def get_possible_starting_points(problem: Problem) -> None:
    """
    Get the possible starting points and calculate entropy.
    :param problem: Problem.
    """

    kernel = np.flip(np.flip(problem.kernel, axis=0), axis=1)
    float_equal_vectorized = np.vectorize(float_equal)

    max_conv = np.sum(np.abs(kernel))

    possible_starts = np.zeros_like(problem.map)

    # for entropy
    n_walls = np.zeros_like(problem.kernel, dtype=int)
    n_halls = np.zeros_like(problem.kernel, dtype=int)
    map_rotated = problem.map

    # rotate the kernel 4 times and convolve it with the map to get starting points
    for rotation_times in range(4):
        conv = fftconvolve(problem.map, kernel, mode='same')
        possible_starts_current = float_equal_vectorized(conv, max_conv)
        possible_starts = np.logical_or(
            possible_starts, possible_starts_current)
        kernel = rotate_matrix(kernel)

        # count halls and walls for entropy
        possible_starts_current_set = set()
        for i in range(possible_starts_current.shape[0]):
            for j in range(possible_starts_current.shape[1]):
                if possible_starts_current[i][j]:
                    possible_starts_current_set.add(
                        rotate_coords((i, j), possible_starts_current.shape, rotation_times, clockwise=True))

        # count walls and halls relative to each possible start
        for start in possible_starts_current_set:
            for i in range(map_rotated.shape[0]):
                for j in range(map_rotated.shape[1]):

                    kernel_i = i - start[0] + \
                        problem.kernel_center()[0]
                    kernel_j = j - start[1] + \
                        problem.kernel_center()[1]

                    if map_rotated[i][j] == WALL:
                        n_walls[kernel_i][kernel_j] += 1
                    elif map_rotated[i][j] == EMPTY:
                        n_halls[kernel_i][kernel_j] += 1

        map_rotated = rotate_matrix(map_rotated, clockwise=True)

    # calculate entropy
    for i in range(problem.entropy.shape[0]):
        for j in range(problem.entropy.shape[1]):
            if n_walls[i][j] + n_halls[i][j] == 0 or problem.kernel[i][j] != 0:
                problem.entropy[i][j] = 0
            else:
                wall_prob = n_walls[i][j] / \
                    (n_walls[i][j] + n_halls[i][j])
                if wall_prob == 0 or wall_prob == 1:
                    problem.entropy[i][j] = 0
                else:
                    problem.entropy[i][j] = \
                        - wall_prob * np.log2(wall_prob) - \
                        (1 - wall_prob) * np.log2(1 - wall_prob)

    problem.possible_starts = possible_starts


def solve(problem: Problem) -> None:
    """
    Solve the given problem.
    :param problem: Problem to be solved.
    """

    find_walls_to_see(problem)
    see(problem)
    get_possible_starting_points(problem)
    get_max_entropy(problem)
    problem.visited[problem.current_position()] = 1

    display = Display(problem)

    while len(problem.max_entropy) > 0:
        get_max_entropy(problem)
        get_the_best_direction(problem)
        problem.move(problem.direction)
        see(problem)
        get_possible_starting_points(problem)
        problem.visited[problem.current_position()] = 1
        display.update(problem)

    display.update(problem, final=True)
    display.show()
