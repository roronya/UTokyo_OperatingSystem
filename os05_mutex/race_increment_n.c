#include <assert.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


/* 大域変数 */
volatile int g = 0;
pthread_mutex_t m;


int main(int argc, char ** argv) {
  long n = (argc > 1 ? atol(argv[1]) : 1000000);
  g = 0;
  pthread_mutex_init(&m, NULL);
#pragma omp parallel
  {
#pragma omp for
    for (long i = 0; i < n; i++) {
      pthread_mutex_lock(&m);
      g++;
      pthread_mutex_unlock(&m);
    }
  }
  printf("g = %d\n", g);
  return 0;
}
