# The Wandering Robot (robot-localization)

An AI simulation of a robot localizing itself in a known 2D maze without a compass, using FFT cross-correlation and entropy-driven exploration. 

This project was originally created as a semestral work for the BI-ZUM.21 course at CTU FIT by Petr Fiedler.

## Description

The scenario presents a robot that has become disoriented within a mapped environment. While it possesses a map of the entire system of corridors (and walls) and highly accurate but limited-range optical sensors, it lacks a compass. Its goal is to navigate through the maze, pinpointing its starting location and direction by matching visual cues to the map. Due to potential environmental symmetries, the robot continuously explores until it has found unique features that determine its exact location (though up to 4 solutions can exist on perfectly symmetrical maps).

## Features / How It Works

### 1. **Localization via Fast Fourier Transform (FFT)**
To determine possible starting positions, the robot uses 2D cross-correlation (convolution) between its scanned local area and the known map. To compute this efficiently in $\mathcal{O}(n \log n)$ time instead of $\mathcal{O}(n^2)$, the project leverages Fast Fourier Transform (FFT) via `scipy.signal`. Walls and corridors are represented numerically ($1$ and $-1$), maximizing convolution scores at valid map matches across all 4 possible rotations.

### 2. **Ray-Traced Vision**
The robot's optical sensors are simulated using Breadth-First Search (BFS) combined with shadow casting (line-of-sight checks). The sensor range is limited, and the robot cannot scan tiles obscured by walls, ensuring realistic exploration limits.

### 3. **Entropy-Driven Exploration & Pathfinding**
The core intelligence of the robot dictates its movement. Instead of wandering randomly, it calculates the **entropy** (information value) of unseen tiles:
- For every assumed starting location and orientation, the robot anticipates what walls and corridors lie in the unscanned areas.
- It computes a probability distribution and its corresponding entropy for these surrounding unknown tiles.
- The robot evaluates accessible boundaries and travels toward the highest-entropy tiles mapping out where it will learn the *most* new information.
- Pathfinding leverages the **A* Search Algorithm**, navigating the maze while balancing maximum informational gain against travel distance penalties.

## Requirements & Installation

The project is built in Python and relies on a few core scientific libraries for mathematics and visualization.

```bash
pip install numpy scipy matplotlib
```

## Usage

You can run the program by providing a map file. The environment layout and the robot's real starting position are defined inside text files located in the `maps/` directory.

If you run the script without arguments, it will prompt you for a file interactively:
```bash
python main.py
```

To run a specific map directly from the CLI:
```bash
python main.py maps/maze.txt
```

### Map File Format
The program reads `.txt` files containing the maze layout, followed by the starting coordinates:
- `X` represents a wall
- ` ` (space) represents a corridor
- The last line specifies the row and column of the start position (e.g., `2, 3`).

*Example (`maps/maze.txt`):*
```text
XXXXXXXXXXXXXXXX
X           X  X
X XXX XXXXX XXXX
X   X     X    X
XXXXXXXXXXXXXXXX
1, 1
```

### Configuration
You can tweak the robot's sensor range and the visualization animation speed in `src/config.py`:
- `VISIBILITY_DISTANCE`: The range of the robot's optical sensors (default: `5`)
- `FPS`: Frames per second for the `matplotlib` visualization (default: `20`)

## Visualization Legend
When the script runs, a live GUI window will pop up showing the robot's state and calculations:
- **Dark Grey / Grey**: Unseen corridors / Unseen walls
- **White / Black**: Scanned corridors / Scanned walls
- **Maroon**: Target start position
- **Indian Red**: Current candidate start locations
- **Medium Slate Blue**: Visited path
- **Lime Green**: High-entropy tiles holding the most expected information
- **Orange**: Current destination edge target

