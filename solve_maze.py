import sys
from util import display_maze, timeit

# Modo de uso:
# - python solve_maze.py [laberinto.txt]

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
#         [0, 1, 1, 0],
#         [0, 1, 1, 0],
#         [0, 0, 0, 0]]

# Se representa una lista de pasos con una list[tuple(int, int)].
# Cada tuple(int, int) representa una posición dentro del laberinto.
# Por ejemplo:
# steps = [(0, 0), (0, 1), (0, 2)]


# read_maze: str -> list(list(int))
# Recibe el nombre de un archivo,
# Devuelve el laberinto que este representa. Si se produce algún error (el
# archivo no existe o el formato del archivo es incorrecto), devuelve [[-1]].
# Ejemplos:
# Entrada: filename="output.txt"; Salida: [[0, 1, 1, 2],
#                                          [0, 1, 1, 0],
#                                          [0, 1, 1, 0],
#                                          [0, 0, 0, 0]]
# Entrada: filename="archivo-inexistente.txt"; Salida: [[-1]]
def read_maze(filename):
    print("Leyendo laberinto desde {0}".format(filename))

    try:
        file = open(filename, "r")
        maze = [[int(n) for n in line.strip()] for line in file.readlines()]
        file.close()
    except FileNotFoundError:
        print("Error: El archivo {0} no existe.".format(filename))
        maze = [[-1]]
    except:
        print("Error: Se ha producido un error tratando de leer el laberinto.")
        print("Verifique que el archivo respeta el formato establecido.")
        maze = [[-1]]

    return maze


# neighbors: int int -> list(tuple(int, int))
# Recibe dos enteros que representan una posición en el laberinto,
# Devuelve una lista con sus 4 "vecinos" (las posiciones a su derecha,
# izquierda, arriba y abajo).
# Ejemplos:
# Entrada: row=10, col=5; Salida: [(10, 4), (9, 5), (10, 6), (11, 5)]
# Entrada: row=0, col=0; Salida: [(0, -1), (-1, 0), (0, 1), (1, 0)]
def neighbors(row, col):
    return [(row, col - 1), (row - 1, col), (row, col + 1), (row + 1, col)]


# sorted_neighbors: int int tuple(int, int) -> list(tuple(int, int))
# Recibe dos enteros que representan una posición en el laberinto y la posición
# del objetivo,
# Devuelve una lista con sus 4 "vecinos" ordenados en orden descendiente con
# respecto a la distancia de cada uno al objetivo.
# Ejemplos:
# Entrada: row=1,                ┐
#          col=0,                ├-> Salida: [(0, 0), (1, -1), (1, 1), (2, 0)]
#          goal_position=(3, 3); ┘
# Entrada: row=3,                ┐
#          col=5,                ├-> Salida: [(3, 4), (2, 5), (4, 5), (3, 6)]
#          goal_position=(9, 7); ┘
def sorted_neighbors(row, col, goal_position):

    # distance_to_goal: tuple(int, int) -> int
    # Recibe una posición en el laberinto,
    # Devuelve el mínimo entre la distancia en columnas y filas que hay entre
    # la posición y el objetivo (ubicado en goal_position).
    # Ejemplos: (con goal_position=(9, 9))
    # Entrada: (0, 0); Salida: 9
    # Entrada: (7, 3); Salida: 2
    def distance_to_goal(position):
        return min(abs(position[0] - goal_position[0]),
                   abs(position[1] - goal_position[1]))

    return sorted(neighbors(row, col), key=distance_to_goal, reverse=True)


# find_goal: list(list(int)) -> tuple(int, int)
# Recibe un laberinto,
# Devuelve la posición en la que se encuentra el objetivo.
# Ejemplos:
# Entrada: maze=[[0, 0, 2, 0], ┐
#                [0, 1, 1, 0], ├-> Salida: (0, 2)
#                [0, 1, 1, 0], |
#                [0, 0, 0, 0]] ┘
# Entrada: maze=[[0, 0, 1], ┐
#                [1, 0, 1], ├-> Salida: (3, 0)
#                [1, 0, 1], |
#                [2, 0, 1]] ┘
def find_goal(maze):
    return [(i, j) for i in range(len(maze)) for j in range(len(maze[0]))
            if maze[i][j] == 2][0]


# solve_maze: list(list(int)) -> list(tuple(int, int))
# Recibe un laberinto,
# Devuelve una lista de pasos que llevan al objetivo del laberinto. Si no tiene
# solución, devuelve una lista vacía.
# Para más información acerca de esta función, ver README.pdf
# Ejemplos:
# Entrada: maze=[[0, 0, 2, 0], ┐
#                [0, 1, 1, 0], ├-> Salida: [(0, 0), (0, 1), (0, 2)]
#                [0, 1, 1, 0], |
#                [0, 0, 0, 0]] ┘
# Entrada: maze=[[0, 1, 1, 1], ┐           [(0, 0), (1, 0), (2, 0),
#                [0, 1, 1, 2], ├-> Salida:  (3, 0), (3, 1), (3, 2),
#                [0, 1, 1, 0], |            (3, 3), (2, 3), (1, 3))]
#                [0, 0, 0, 0]] ┘
# Entrada: maze=[[0, 1, 0, 0], ┐
#                [1, 1, 0, 0], ├-> Salida: []
#                [0, 0, 0, 0], |
#                [0, 0, 0, 2]] ┘
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
    if maze == [[-1]]:
        sys.exit(-1)

    steps = solve_maze(maze)

    if steps:
        print(steps)
    else:
        print("Error: No es posible resolver el laberinto")

    if input("Desea visualizar el resultado? (si/NO): ") == "si":
        display_maze(maze, steps)
