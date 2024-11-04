#include <assert.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>


/* 大域変数 */
volatile int g = 0;

/* スレッドの開始関数 */
void * f(void * arg_) {
  long * arg = arg_;
  long n = arg[0];
  for (long i = 0; i < n; i++) {
    g++;
  }
  return 0;
}


int main(int argc, char ** argv) {
  long n = (argc > 1 ? atol(argv[1]) : 1000000);
  long arg[1] = { n };
  g = 0;
  /* スレッドを作る */
  const int nthreads = 2;
  pthread_t child_thread_id[nthreads];
  for (int i = 0; i < nthreads; i++) {
    if (pthread_create(&child_thread_id[i], 0, f, arg))
      err(1, "pthread_create");
  }
  /* 終了待ち */
  for (int i = 0; i < nthreads; i++) {
    void * ret = 0;
    if (pthread_join(child_thread_id[i], &ret))
      err(1, "pthread_join");
  }
  printf("g = %d\n", g);
  return 0;
}
