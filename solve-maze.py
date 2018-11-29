from util import display_maze, timeit
import sys


def parse_maze(filename="maze.txt"):
    file = open(filename, "r")
    maze = [[int(n) for n in line.strip()] for line in file.readlines()]
    file.close()

    return maze


def neighbors(row, col):
    return [(row, col - 1), (row - 1, col), (row, col + 1), (row + 1, col)]


@timeit
def solve_maze_stack(maze):
    stack = [(0, 0)]
    steps = []
    done = False

    while not done and len(stack):
        row, col = stack.pop()

        if row == -1 and col == -1:
            steps.pop()
        elif row == -1 or row == len(maze) or col == -1 or col == len(maze[0]):
            pass  # print("Out of bounds at ({0}, {1})".format(row, col))
        elif maze[row][col] == -1:
            pass  # print("visited at ({0}, {1})".format(row, col))
        elif maze[row][col] == 0:
            # print("visiting ({0}, {1})".format(row, col))
            steps.append((row, col))
            maze[row][col] = -1

            stack.append((-1, -1))
            for neighbor in neighbors(row, col):
                stack.append(neighbor)
        elif maze[row][col] == 1:
            pass  # print("wall at ({0}, {1})".format(row, col))
        elif maze[row][col] == 2:
            # print("goal at ({0}, {1})".format(row, col))
            steps.append((row, col))
            done = True

    return steps

if __name__ == "__main__":
    maze_file = sys.argv[1] if len(sys.argv) == 2 else "maze.txt"
    maze = parse_maze(maze_file)
    steps = solve_maze_stack(maze)
    display_maze(maze, steps)
