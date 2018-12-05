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
#
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

# Se representa una lista de pasos con una list(tuple(int, int)).
# Cada tuple(int, int) representa una posición dentro del laberinto.
# Las listas de pasos representan las posiciones por las que hay que pasar
# para llegar desde la posición inicial (0, 0) hasta el objetivo.
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
# El orden en que devuelve los vecinos es importante: IZQUIERDA, ARRIBA,
# DERECHA, ABAJO. Elegí este orden ya que la función solve_maze retira el
# último elemento de la pila (stack) en cada iteración, por lo cual este orden
# lleva a que primero se explore hacia ABAJO, luego DERECHA, luego ARRIBA y por
# último IZQUIERDA. Podría haberse establecido un orden distinto, pero como se
# comienza el laberinto en la esquina superior izquierda  (0, 0), tiene sentido
# buscar el objetivo tratando de alejarse del origen.
# Ejemplos:
# Entrada: row=10, col=5; Salida: [(10, 4), (9, 5), (10, 6), (11, 5)]
# Entrada: row=0, col=0; Salida: [(0, -1), (-1, 0), (0, 1), (1, 0)]
def neighbors(row, col):
    return [(row, col - 1), (row - 1, col), (row, col + 1), (row + 1, col)]


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
    stack = [(0, 0)]
    steps = []
    done = False

    while not done and len(stack):
        current_row, current_col = stack.pop()

        if current_row == -1 and current_col == -1:
            steps.pop()
        elif 0 <= current_row < len(maze) and 0 <= current_col < len(maze[0]):
            if maze[current_row][current_col] == 0:
                steps.append((current_row, current_col))
                maze[current_row][current_col] = -1

                stack.append((-1, -1))
                for neighbor in neighbors(current_row, current_col):
                    stack.append(neighbor)

            elif maze[current_row][current_col] == 2:
                steps.append((current_row, current_col))
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
