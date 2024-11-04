#include <assert.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


/* 大域変数 */
volatile int g = 0;



int main(int argc, char ** argv) {
  long n = (argc > 1 ? atol(argv[1]) : 1000000);
  g = 0;
#pragma omp parallel
  {
    for (long i = 0; i < n; i++) {
      g++;
    }
  }
  printf("g = %d\n", g);
  return 0;
}
