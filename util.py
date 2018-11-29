import time
from termcolor import colored


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
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
