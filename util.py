import time
from termcolor import colored


# timeit es un decorador para ver el tiempo de ejecución de la función que
# decora.
# Por ejemplo:
# @timeit
# def sleep_5():
#   time.sleep(5)
#
# >>> sleep_5()
# La función sleep_5 tardó 5005.15 ms en correr
def timeit(method):
    def timed(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()

        delta_time = (end - start) * 1000
        print("La función {0} tardó {1:2.2f} ms en correr"
              .format(method.__name__, delta_time))

        return result

    return timed


# display_maze: list(list(int)) list(tuple(int, int)) -> None
# Recibe un laberinto y una lista de pasos,
# Muestra el laberinto y el recorrido realizado por la lista de pasos.
# Ejemplos:
# Entrada: maze=[[0, 1, 1, 1],              ┐
#                [0, 1, 1, 2],              |
#                [0, 1, 1, 0],              |
#                [0, 0, 0, 0]],             ├-> Salida: None
#          steps=[(0, 0), (1, 0), (2, 0),   |
#                 (3, 0), (3, 1), (3, 2),   |
#                 (3, 3), (2, 3), (1, 3))]; ┘
def display_maze(maze, steps):
    print("\n".join(" ".join(colourful(maze, steps, i, j)
                             for j in range(len(maze[0])))
          for i in range(len(maze))))


# pretty_cell: list(list(int)) list(tuple(int, int)) int int -> str
# Recibe un laberinto, una lista de pasos, y dos enteros que representan una
# posición en el laberinto,
# Devuelve:
# - "+" de color verde si la posición pertenece a la lista de pasos
# - "0" de color azul si en la posición hay un -1
# - "0" de color blanco si en la posición hay un 0
# - "1" de color rojo si no se cumplió ninguna de las condiciones anteriores
# Ejemplos:
# Entrada: maze=[[0, 1, 1, 1],              ┐
#                [0, 1, 1, 2],              |
#                [0, 1, 1, 0],              |
#                [0, 0, 0, 0]],             ├-> Salida: "+" (de color verde)
#          steps=[(0, 0), (1, 0), (2, 0),   |
#                 (3, 0), (3, 1), (3, 2),   |
#                 (3, 3), (2, 3), (1, 3))], |
#          row=3, col=3;                    ┘
def colourful(maze, steps, row, col):
    if (row, col) in steps:
        return colored("+", color="green")
    elif maze[row][col] == -1:
        return colored("0", color="blue")
    elif maze[row][col] == 0:
        return colored("0", color="white")
    else:
        return colored("1", color="red")
