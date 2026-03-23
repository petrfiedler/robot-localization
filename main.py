"""

BI-ZUM.21 Semestral Work: 
The Wandering Robot

This challenge presents a scenario in which a robot has become disoriented
within a labyrinthine environment and must rely on visual cues to orient itself
and pinpoint its location on the map. The robot possesses highly accurate
optical sensors, but it relies on a pre-existing map of the environment to
navigate. The task at hand is to guide the robot's orientation within the
mapped environment using the visual cues it observes, which may be quite
uniform.

Petr Fiedler
2023

"""

import sys
from src.read_input import read_input


def main() -> bool:
    """
    Main function.
    :return: 0 if input was read successfully, 1 otherwise.
    """

    # read input and solve the problem
    return not read_input()


if __name__ == '__main__':
    sys.exit(main())
