import time
from termcolor import colored


def timeit(method):

    def timed(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()

        duration = (end - start) * 1000
        print("{0} tardó {1:2.2f} ms en correr".format(method.__name__, duration))

        return result

    return timed


def display_maze(maze, steps):
    print("\n".join(" ".join(pretty_cell(maze, steps, i, j)
                             for j in range(len(maze[0])))
          for i in range(len(maze))))


def pretty_cell(maze, steps, i, j):
    if (i, j) in steps:
        return colored("+", color="green")
    if maze[i][j] == -1:
        return colored("O", color="blue")
    if maze[i][j] == 0:
        return colored(" ", color="white")
    return colored("X", color="red")
