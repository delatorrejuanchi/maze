import pytest

# Importamos las funciones que vamos a testear
from solve_maze import neighbors, sorted_neighbors, find_goal, solve_maze


def test_neighbors():
    row_1, col_1 = 10, 5
    neighbors_1 = [(10, 4), (9, 5), (10, 6), (11, 5)]

    row_2, col_2 = 0, 0
    neighbors_2 = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    assert(neighbors(row_1, col_1) == neighbors_1)
    assert(neighbors(row_2, col_2) == neighbors_2)


def test_sorted_neighbors():
    row_1, col_1, goal_1 = 1, 0, (3, 3)
    sorted_neighbors_1 = [(0, 0), (1, -1), (1, 1), (2, 0)]

    row_2, col_2, goal_2 = 3, 5, (9, 7)
    sorted_neighbors_2 = [(3, 4), (2, 5), (4, 5), (3, 6)]

    assert(sorted_neighbors(row_1, col_1, goal_1) == sorted_neighbors_1)
    assert(sorted_neighbors(row_2, col_2, goal_2) == sorted_neighbors_2)


def test_find_goal():
    maze_1 = [[0, 0, 2, 0],
              [0, 1, 1, 0],
              [0, 1, 1, 0],
              [0, 0, 0, 0]]
    goal_1 = (0, 2)

    maze_2 = [[0, 0, 1],
              [1, 0, 1],
              [1, 0, 1],
              [2, 0, 1]]
    goal_2 = (3, 0)

    maze_3 = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 0, 0, 1, 0, 0, 0, 1, 0, 2]]
    goal_3 = (9, 9)

    assert(find_goal(maze_1) == goal_1)
    assert(find_goal(maze_2) == goal_2)
    assert(find_goal(maze_3) == goal_3)


def test_solve_maze():
    maze_1 = [[0, 0, 2, 0],
              [0, 1, 1, 0],
              [0, 1, 1, 0],
              [0, 0, 0, 0]]
    steps_1 = [(0, 0), (0, 1), (0, 2)]

    maze_2 = [[0, 0, 1],
              [1, 0, 1],
              [1, 0, 1],
              [2, 0, 1]]
    steps_2 = [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0)]

    maze_3 = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
              [0, 0, 0, 1, 0, 0, 0, 1, 0, 2]]
    steps_3 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
               (8, 0), (9, 0), (9, 1), (9, 2), (8, 2), (7, 2), (6, 2), (5, 2),
               (4, 2), (3, 2), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4), (1, 4),
               (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
               (9, 5), (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (3, 6),
               (2, 6), (1, 6), (0, 6), (0, 7), (0, 8), (1, 8), (2, 8), (3, 8),
               (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (9, 9)]

    assert(solve_maze(maze_1) == steps_1)
    assert(solve_maze(maze_2) == steps_2)
    assert(solve_maze(maze_3) == steps_3)
