import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from src.problem import Problem
from src.helpers import add_tuples, subtract_tuples
from src.config import *
from src.constants import *

legend = {
    CLR_EMPTY_UNSEEN: 'Hall (unseen)',
    CLR_WALL_UNSEEN: 'Wall (unseen)',
    CLR_EMPTY_SEEN: 'Hall (seen)',
    CLR_WALL_SEEN: 'Wall (seen)',
    CLR_ENTROPY: 'Max entropy',
    CLR_ENTROPY_OOB: 'Max entropy (out of bounds)',
    CLR_TARGET: 'Current target',
    CLR_START: 'Start',
    CLR_POSSIBLE_START: 'Possible start',
    CLR_VISITED: 'Visited',
    CLR_CURRENT: 'Robot',
}

colors = list(legend.keys())

color_code = {color: index for index, color in enumerate(colors)}

cmap = LinearSegmentedColormap.from_list('grid_map', colors)
norm = plt.Normalize(0, len(colors) - 1)


def show_static(problem: Problem) -> None:
    """
    Show the problem in a static way.

    :param problem: Problem to show.
    """

    grid = problem.map.copy()
    grid[grid == EMPTY] = color_code[CLR_EMPTY_UNSEEN]
    grid[grid == WALL] = color_code[CLR_WALL_UNSEEN]

    seen = np.zeros_like(problem.map, dtype=int)
    seen[problem.seen] = problem.map[problem.seen]
    grid[seen == EMPTY] = color_code[CLR_EMPTY_SEEN]
    grid[seen == WALL] = color_code[CLR_WALL_SEEN]

    grid[problem.possible_starts] = color_code[CLR_POSSIBLE_START]

    grid[problem.visited] = color_code[CLR_VISITED]

    grid[problem.start] = color_code[CLR_START]
    grid[problem.current_position()] = color_code[CLR_CURRENT]

    plt.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)
    plt.axis('off')
    plt.show()


class Display:
    """
    Display the problem animated.
    """

    def __init__(self, problem):
        """
        Initialize the display with the initial position.

        :param problem: Problem to display.
        """

        grid = self.calculate_grid(problem)

        self.output = plt.imshow(
            grid, interpolation='nearest', cmap=cmap, norm=norm)

        plt.axis('off')

        # make room for legend
        plt.subplots_adjust(right=0.7)

        # show legend
        plt.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=cmap(norm(color_code[color]))) for color in colors],
                   labels=[legend[color] for color in colors], loc='center right', ncol=1, bbox_to_anchor=(1.5, .5),
                   fontsize='small')

        # set window title
        plt.gcf().canvas.set_window_title(TITLE)

        # terminate the program when the window is closed
        plt.connect('close_event', self.handle_close)

        # maximize the window
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()

    def handle_close(self, event):
        """
        Terminate the program when the window is closed.

        :param event: The event that triggered the closing.
        """

        exit(0)

    def update(self, problem, final=False):
        """
        Update the display with the current state.

        :param problem: The problem to be displayed.
        :param final: Whether the problem is in its final state.
        """

        grid = self.calculate_grid(problem, final)
        self.output.set_data(grid)
        plt.draw()
        plt.pause(1/FPS)

    def show(self):
        """
        Show the display.
        """

        plt.show()

    def calculate_grid(self, problem, final=False):
        """
        Calculate the grid to be displayed.

        :param problem: The problem to be displayed.
        :param final: Whether the problem is in its final state.
        """

        grid = problem.map.copy()
        grid[grid == EMPTY] = color_code[CLR_EMPTY_UNSEEN]
        grid[grid == WALL] = color_code[CLR_WALL_UNSEEN]

        seen = np.zeros_like(problem.map, dtype=int)
        seen[problem.seen] = problem.map[problem.seen]
        grid[seen == EMPTY] = color_code[CLR_EMPTY_SEEN]
        grid[seen == WALL] = color_code[CLR_WALL_SEEN]

        grid[problem.possible_starts] = color_code[CLR_POSSIBLE_START]

        grid[problem.visited] = color_code[CLR_VISITED]

        grid[problem.start] = color_code[CLR_START]

        grid[problem.current_position()] = color_code[CLR_CURRENT]

        for position in problem.max_entropy:
            display_position = add_tuples(
                problem.start, subtract_tuples(position, problem.kernel_center()))

            trimmed_position = list(display_position)
            trimmed_position[0] = max(
                0, min(display_position[0], problem.map.shape[0] - 1))
            trimmed_position[1] = max(
                0, min(display_position[1], problem.map.shape[1] - 1))

            trimmed_position = tuple(trimmed_position)

            if display_position == trimmed_position:
                grid[display_position] = color_code[CLR_ENTROPY]
            else:
                grid[trimmed_position] = color_code[CLR_ENTROPY_OOB]

        if final:
            grid[problem.possible_starts] = color_code[CLR_POSSIBLE_START]
            grid[problem.start] = color_code[CLR_START]
        else:
            grid[problem.target] = color_code[CLR_TARGET]

        return grid
