#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// Modo de uso:
// - ./generate-maze [archivo-de-entrada.txt] [archivo-de-salida.txt]
// El archivo de entrada debe tener el siguiente formato:
// - La primer línea expresa las dimensiones del laberinto separadas por un espacio (máximo: 15 15)
// - La segunda línea expresa las coordenadas del objetivo separadas por un espacio (máximo: 20 20)
// - El resto de las líneas expresan las coordenadas de las paredes separadas un espacio (máximo 20 líneas)
// Por ejemplo: (archivo-de-entrada.txt)
//   4 4        (--> El laberinto generado será 4x4)
//   0 3        (--> El objetivo se encontrará en la posición (0, 3), es decir fila 0 columna 3)
//   0 1        (--> Habrá una pared en la posición (0, 1))
//   1 1        (--> Habrá una pared en la posición (1, 1))
//   2 1        (--> Habrá una pared en la posición (2, 1))
//   0 2        (--> Habrá una pared en la posición (0, 2))
//   1 2        (--> Habrá una pared en la posición (1, 2))
//   2 2        (--> Habrá una pared en la posición (2, 2))
//
// Genera: (archivo-de-salida.txt)
//   0112
//   0110
//   0110
//   0000
//
// No es necesario que el archivo de salida exista con anterioridad.

// Se representa un laberinto con una int[15][15] (ya que ese es el máximo tamaño establecido) junto con dos enteros
// entre 0 y 15 (nRows y nCols) que determinan el tamaño real del mismo.
// Para todo i entre 0 y nRows, y todo j entre 0 y nCols:
// - maze[i][j] == 0 representa una posición vacía.
// - maze[i][j] == 1 representa una posición con una pared.
// - maze[i][j] == 2 representa el objetivo.

// Se representa una lista de coordenadas con una int[22][2]. Tiene 22 filas porque el máximo de lineas que puede tener
// el archivo a leer es 1 (tamaño) + 1 (posición del objetivo) + 20 (máxima cantidad de paredes) = 22. Tiene 2 columnas
// porque la primera tiene los números de las filas y la segunda los de las columnas.
// La primera fila contiene las dimensiones del laberinto.
// La segunda fila contiene las coordenadas del objetivo.
// El resto de las filas (máximo 20) contiene las coordenadas de las paredes.

// loadCoordinates: char[] int[22][2] -> int
// Recibe el nombre del archivo a leer y una lista de coordenadas,
// Si el archivo existe, escribe las coordenadas presentes en el archivo a la lista de coordenadas (máximo 22) y
// devuelve la cantidad de coordenadas leídas (entre 0 y 22). Si no, devuelve -1.
// Ejemplos:
// Entrada: filename[]="input.txt", coordinates[22][2]={ ... }; Salida: #cantidad-de-coordenadas-leidas
// Entrada: filename[]="archivo-no-existente.txt", coordinates[22][2]={ ... }; Salida: -1
int loadCoordinates(char filename[], int coordinates[22][2]) {
  FILE *inputFile;
  inputFile = fopen(filename, "r");

  if (inputFile == NULL) {
    printf("Error: El archivo %s no existe!\n", filename);
    return -1;
  }

  int row = -1, col = -1;
  int i = 0;
  while (fscanf(inputFile, "%d %d\n", &row, &col) != EOF && i < 22) {
    coordinates[i][0] = row;
    coordinates[i][1] = col;
    i++;
  }

  fclose(inputFile);

  printf("Se ha leído el archivo %s exitosamente.\n", filename);

  return i;
}

// areCoordinatesValid: int[22][2] int -> int
// Recibe una lista de coordenadas y la cantidad de coordenadas,
// Devuelve 1 si las coordenadas son válidas, 0 en caso contrario.
// Ejemplos:
// Entrada: coordinates[22][2]={ ... }, numCoordinates=1; Salida: 0
// Entrada: coordinates[22][2]={ {-5 4}, ... }, numCoordinates=5; Salida: 0
// Entrada: coordinates[22][2]={ {10, 10}, {15, 5}, ... }, numCoordinates=7; Salida: 0
// Entrada: coordinates[22][2]={ {10, 10}, {9, 9}, {-1, 15}, ... }, numCoordinates=1; Salida: 0
// Entrada: coordinates[22][2]={ {10, 10}, {9, 9}, {3, 3}, ... }, numCoordinates=3; Salida: 1
int areCoordinatesValid(int coordinates[22][2], int numCoordinates) {
  if (numCoordinates < 2) {
    printf("Error: Como mínimo, deben estar presentes las dimensiones del laberinto y las coordenadas del objetivo\n");
    return 0;
  }

  int nRows = coordinates[0][0];
  int nCols = coordinates[0][1];
  int goalRow = coordinates[1][0];
  int goalCol = coordinates[1][1];

  if (nRows <= 0 || nCols <= 0) {
    printf("Error: Las dimensiones del laberinto deben ser positivas.\n");
    return 0;
  }

  if (goalRow < 0 || goalRow >= nRows || goalCol < 0 || goalCol >= nCols) {
    printf("Error: Las coordenadas del objetivo son inválidas.\n");
    return 0;
  }

  int numBadWalls = 0;
  for(int i = 2; i < numCoordinates; i++) {
    if (coordinates[i][0] < 0 || coordinates[i][0] >= nRows || coordinates[i][1] < 0 || coordinates[i][1] >= nCols) {
      numBadWalls++;
    }
  }

  if (numBadWalls) {
    printf("Error: Las coordenadas de %d pared(es) son inválidas.\n", numBadWalls);
    return 0;
  }

  return 1;
}

// updateMaze: int[15][15] int[22][2] int -> void
// Recibe un laberinto, una lista de coordenadas y una cantidad de coordenadas,
// Escribe 1 en las posiciones con paredes, 2 en la posición del objetivo, 0 en el resto de las posiciones del
// laberinto (hasta los límites establecidos por la dimensión del mismo).
// Ejemplos:
// Entrada: maze[15][15]={ ... }, coordinates[22][2]={ ... }, numCoordinates=15; Salida: void
void updateMaze(int maze[15][15], int coordinates[22][2], int numCoordinates) {
  for(int i = 0; i < coordinates[0][0]; i++) {
    for(int j = 0; j < coordinates[0][1]; j++) {
      maze[i][j] = 0;
    }
  }

  for(int i = 2; i < numCoordinates; i++) {
    maze[coordinates[i][0]][coordinates[i][1]] = 1;
  }

  int goalRow = coordinates[1][0];
  int goalCol = coordinates[1][1];

  maze[goalRow][goalCol] = 2;
}

// writeToFile: char[] int[15][15] int int -> void
// Recibe el nombre del archivo donde se escribirá el laberinto, el laberinto y la cantidad de filas y columnas de este,
// Escribe el laberinto al archivo.
// Ejemplos:
// Entrada: filename[]="output.txt", maze[15][15]={ ... }, nRows=12, nCols=5; Salida: void
void writeToFile(char filename[], int maze[15][15], int nRows, int nCols) {
  FILE *outputFile;
  outputFile = fopen(filename, "w+");

  for(int i = 0; i < nRows; i++) {
    for(int j = 0; j < nCols; j++) {
      fprintf(outputFile, "%d", maze[i][j]);
    }
    fprintf(outputFile, "\n");
  }

  printf("El laberinto ha sido escrito a %s exitosamente.\n", filename);

  fclose(outputFile);
}

// runAsserts: -> void
// Corre los casos de prueba
void runAsserts() {
  // no hay casos de prueba para loadCoordinates y writeToFile debido a que manejan archivos

  // areCoordinatesValid(int coordinates[22][2], int numCoordinates) -> int
  int coordinates[22][2];
  coordinates[0][0] = -1, coordinates[0][1] = 10;

  assert(areCoordinatesValid(coordinates, 1) == 0); // como mínimo deben estar presentes tamaño y posición del objetivo

  coordinates[1][0] = 12, coordinates[1][1] = 9; // agregamos la posición del objetivo, pero
  assert(areCoordinatesValid(coordinates, 2) == 0); // las dimensiones del laberinto deben ser positivas

  coordinates[0][0] = 10; // corregimos las dimensiones del laberinto, pero
  assert(areCoordinatesValid(coordinates, 2) == 0); // las coordenadas del objetivo son inválidas

  coordinates[1][0] = 8; // corregimos las coordenadas del objetivo
  assert(areCoordinatesValid(coordinates, 2) == 1); // esto debería funcionar!

  coordinates[2][0] = 10, coordinates[2][1] = 5; // agregamos una pared en (10, 5), pero
  assert(areCoordinatesValid(coordinates, 3) == 0); // las coordenadas de 1 pared son inválidas

  coordinates[2][0] = 5; // corregimos las coordenadas de la pared, ahora está en (5, 5)
  assert(areCoordinatesValid(coordinates, 3) == 1); // esto debería funcionar!

  coordinates[3][0] = 1, coordinates[3][1] = 4; // agregamos una pared en (1, 4)
  coordinates[4][0] = 3, coordinates[4][1] = 5; // agregamos una pared en (3, 5)
  coordinates[5][0] = 6, coordinates[5][1] = 7; // agregamos una pared en (6, 7)
  coordinates[6][0] = 1, coordinates[6][1] = 3; // agregamos una pared en (1, 3)
  assert(areCoordinatesValid(coordinates, 7) == 1); // esto debería funcionar!

  // updateMaze(int maze[15][15], int coordinates[22][2], int numCoordinates) -> void
  int maze[15][15];

  updateMaze(maze, coordinates, 2);
  assert(maze[0][0] == 0); // la posición (0, 0) debería tener un 0
  assert(maze[0][8] == 0); // la posición (0, 8) también debería tener un 0, etc.
  assert(maze[8][9] == 2); // la posición (8, 9) debería tener un 2

  updateMaze(maze, coordinates, 5);
  assert(maze[5][5] == 1); // la posición (5, 5) debería tener un 1, etc.
  assert(maze[1][4] == 1); // la posición (1, 4) también debería tener un 1
  assert(maze[3][5] == 1); // la posición (3, 5) también debería tener un 1
}

int main(int argc, char *argv[]) {
  // Por defecto, desactivo los tests para no confundir al usuario con los mensajes de error generados por las
  // funciones testeadas
  // runAsserts();

  if (argc != 3) {
    printf("Error: El número de argumentos ingresados es incorrecto.\n");
    printf("Modo de uso: %s [archivo-de-entrada.txt] [archivo-de-salida.txt]\n", argv[0]);
    return -1;
  }

  int coordinates[22][2]; // coordinates tiene 22 filas porque el máximo de lineas que puede tener el archivo a leer
                          // es 1 (tamaño) + 1 (posición del objetivo) + 20 (máxima cantidad de paredes) = 22
  int maze[15][15]; // maze tiene 15 filas y 15 columnas porque se estableció ese tamaño como el máximo

  int numCoordinates = loadCoordinates(argv[1], coordinates);
  int areValid = areCoordinatesValid(coordinates, numCoordinates);
  if (!areValid) {
    printf("Hubo errores leyendo el archivo. Consulte README.pdf para información sobre el formato que debe tener.\n");
    return -1;
  }
  updateMaze(maze, coordinates, numCoordinates);
  writeToFile(argv[2], maze, coordinates[0][0], coordinates[0][1]);

  return 0;
}
