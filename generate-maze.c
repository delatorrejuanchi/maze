#include <stdio.h>
#include <stdlib.h>

// TODO: write comments
// TODO: refactor, limit size and number of walls
// TODO: add checks to ensure objectiveRow and objectiveCol are valid
// TODO: rename objective to goal

int main(int argc, char const *argv[]) {
  if (argc != 3) {
    printf("Error: El número de argumentos ingresados es incorrecto.\n");
    printf("Modo de uso: %s [archivo-de-entrada.txt] [archivo-de-salida.txt]\n", argv[0]);
    return -1;
  }

  FILE *inputFile;
  inputFile = fopen(argv[1], "r");

  if (inputFile == NULL) {
    printf("Error: El archivo %s no existe!\n", argv[1]);
    return -1;
  }

  int nRows, nCols;
  fscanf(inputFile, "%d %d\n", &nRows, &nCols);

  int maze[nRows][nCols];

  for(int i = 0; i < nRows; i++) {
    for(int j = 0; j < nCols; j++) {
      maze[i][j] = 0;
    }
  }

  int objectiveRow, objectiveCol;
  fscanf(inputFile, "%d %d\n", &objectiveRow, &objectiveCol);

  int wallRow, wallCol;
  while (fscanf(inputFile, "%d %d\n", &wallRow, &wallCol) != EOF) {
    maze[wallRow][wallCol] = 1;
  }

  maze[objectiveRow][objectiveCol] = 2;

  fclose(inputFile);

  FILE *outputFile;
  outputFile = fopen(argv[2], "w+");

  for(int i = 0; i < nRows; i++) {
    for(int j = 0; j < nCols; j++) {
      printf("%d", maze[i][j]);
      fprintf(outputFile, "%d", maze[i][j]);
    }
    printf("\n");
    fprintf(outputFile, "\n");
  }

  printf("El laberinto ha sido escrito a %s exitosamente\n", argv[2]);

  fclose(outputFile);

  return 0;
}
