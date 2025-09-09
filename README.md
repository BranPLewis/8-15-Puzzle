# A* N-Puzzle Solver

## What is the N-Puzzle?

The N-Puzzle is a classic sliding puzzle that consists of a grid of numbered tiles with one tile missing.
The most common versions are the 8-puzzle (a 3x3 grid) and the 15-puzzle (a 4x4 grid). The objective is to
rearrange the tiles from a scrambled starting configuration into a sorted goal configuration by sliding
tiles into the empty space.

## About This Program

This program is a Python-based solver for the N-Puzzle that uses the A* search algorithm to find the
shortest solution path from a given initial state to the goal state. A* is an intelligent search algorithm
that efficiently explores the possible moves by using a heuristic to guide it toward the solution.

This implementation allows you to choose from three different heuristics:

* Manhattan Distance: A highly effective heuristic that calculates the sum of the distances of each tile
from its goal position.
* Misplaced Tiles: A simpler heuristic that counts the number of tiles that are not in their correct final
position.
* Zero Heuristic (Uniform Cost Search): A baseline search that explores paths based only on their current
cost, without any guidance toward the goal.

## How to Run the Program

You can run the solver from the command line. The script requires a domain argument and accepts optional
arguments for the heuristic and the number of boards to solve.

### Command-Line Arguments

* domain (Required)
  - Description: Specifies the problem domain. For this program, it must always be puzzle.
  - Usage: python main.py puzzle
* -H, --heuristic (Optional)
  - Description: Chooses the heuristic function to guide the A* search.
  - Options: manhattan, misplaced, weighted_manhattan, zero
  - Default: manhattan
* -n, --number (Optional)
  - Description: The number of predefined puzzle boards to solve in sequence.
  - Default: 1


### Examples

1. Solve one puzzle with the default Manhattan heuristic:

 - python main.py puzzle

2. Solve five puzzles using the Misplaced Tiles heuristic:

 - python main.py puzzle --heuristic misplaced --boards 5

3. Run a Uniform Cost Search (zero heuristic) on the first ten puzzles:

 - python main.py puzzle -H zero -n 10

4. Get help and see all available options:

 - python main.py -h
