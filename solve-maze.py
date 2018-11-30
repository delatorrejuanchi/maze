import sys
from util import display_maze, timeit

# TODO: write examples
# TODO: write tests

# Modo de uso:
# - python solve-maze.py [laberinto.txt]

# El archivo a recibir debe contener un laberinto de la forma:
#   0100010001
#   0101010101
#   0101010101
#   0101010101
#   0101010101
#   0101010101
#   0101010101
#   0101010101
#   0101010101
#   0001000102
# Los 0 representan posiciones vacías, los 1 paredes y el 2 representa el
# objetivo. El laberinto puede tener tantas filas y columnas como se desee.

# Se representa una posición con una tuple(int, int). El primer elemento
# representa el número de fila, y el segundo el número de columna.
# Por ejemplo:
# origin = (0, 0)
# position = (13, 5)

# Se representa un laberinto con una list(list(int)).
# - maze[i][j] == 0 representa una posición vacía.
# - maze[i][j] == 1 representa una posición con una pared.
# - maze[i][j] == 2 representa el objetivo.
# - maze[i][j] == -1 representa una posición que ya ha sido visitada.
# Por ejemplo:
# maze = [[0, 0, 2, 0],
#         [0, 1, 1, 0]
#         [0, 1, 1, 0]
#         [0, 0, 0, 0]]

# Se representa una lista de pasos con una list[tuple(int, int)].
# Cada tuple(int, int) representa una posición dentro del laberinto.
# Por ejemplo:
# steps = [(0, 0), (0, 1), (0, 2)]


# read_maze: str -> list(list(int))
# Recibe el nombre de un archivo,
# Devuelve el laberinto que este representa.
def read_maze(filename):
    print("Leyendo laberinto desde {0}".format(filename))

    file = open(filename, "r")
    maze = [[int(n) for n in line.strip()] for line in file.readlines()]
    file.close()

    return maze


# neighbors: int int -> list(tuple(int, int))
# Recibe dos enteros que representan una posición en el laberinto,
# Devuelve una lista con sus 4 "vecinos" (las posiciones a su derecha,
# izquierda, arriba y abajo)
def neighbors(row, col):
    return [(row, col - 1), (row - 1, col), (row, col + 1), (row + 1, col)]


# sorted_neighbors: int int tuple(int, int) -> list(tuple(int, int))
# Recibe dos enteros que representan una posición en el laberinto y la posición
# del objetivo,
# Devuelve una lista con sus 4 "vecinos" ordenados en orden ascendiente con
# respecto a la distancia de cada uno al objetivo.
def sorted_neighbors(row, col, goal_position):

    # distance_to_goal: tuple(int, int) -> int
    # Recibe una posición en el laberinto,
    # Devuelve el mínimo entre la distancia en columnas y filas que hay entre
    # la posición y el objetivo.
    def distance_to_goal(position):
        return min(abs(position[0] - goal_position[0]),
                   abs(position[1] - goal_position[1]))

    return sorted(neighbors(row, col), key=distance_to_goal, reverse=True)


# find_goal: list(list(int)) -> tuple(int, int)
# Recibe un laberinto,
# Devuelve la posición en la que se encuentra el objetivo.
def find_goal(maze):
    return [(i, j) for i in range(len(maze)) for j in range(len(maze[0]))
            if maze[i][j] == 2][0]


# solve_maze: list(list(int)) -> list(tuple(int, int))
# Recibe un laberinto,
# Devuelve una lista de pasos que llevan al objetivo del laberinto.
# Para más información acerca de esta función, ver README.pdf
@timeit
def solve_maze(maze):
    goal_position = find_goal(maze)
    stack = [(0, 0)]
    steps = []
    done = False

    while not done and len(stack):
        row, col = stack.pop()

        if row == -1 and col == -1:
            steps.pop()
        elif 0 <= row < len(maze) and 0 <= col < len(maze[0]):
            if maze[row][col] == 0:
                steps.append((row, col))
                maze[row][col] = -1

                stack.append((-1, -1))
                for neighbor in sorted_neighbors(row, col, goal_position):
                    stack.append(neighbor)

            elif maze[row][col] == 2:
                steps.append((row, col))
                done = True

    return steps


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: el número de argumentos ingresados es incorrecto.")
        print("Modo de uso: python {0} [laberinto.txt]".format(sys.argv[0]))
        sys.exit(-1)

    maze_file = sys.argv[1]

    maze = read_maze(maze_file)
    steps = solve_maze(maze)

    if steps:
        print(steps)
    else:
        print("Error: No es posible resolver el laberinto")

    if input("Desea visualizar el resultado? (si/NO): ") == "si":
        display_maze(maze, steps)
