#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <omp.h>

pthread_mutex_t m;

int check_prime(long n) {
  for (long d = 2; d * d <= n; d++) {
    if (n % d == 0) return 0;
  }
  return n > 1;
}

void count_primes(long a, long b, long * s) {
#pragma omp for
  for (long n = a; n < b; n++) {
    if (check_prime(n)) {
      pthread_mutex_lock(&m);
      *s += 1;
      pthread_mutex_unlock(&m);

    }
  }
}


double cur_time() {
  struct timespec ts[1];
  clock_gettime(CLOCK_REALTIME, ts);
  return ts->tv_nsec * 1.0E-9 + ts->tv_sec;
}

int main(int argc, char ** argv) {
  long i = 1;
  long a = (argc > i ? atol(argv[i]) : 1000000); i++;
  long b = (argc > i ? atol(argv[i]) : 2000000); i++;
  long s = 0;
  double t0 = cur_time();
  pthread_mutex_init(&m, NULL);

#pragma omp parallel            
  {
    /* 起動時に環境変数OMP_NUM_THREADS=xxx で指定した
       個数のスレッドが作られ, 各々が以下の文 { ... }
       を実行する.
       関数内のpragma omp for 下のfor文をそれらのスレッドが
       分割して実行する */
    count_primes(a, b, &s);
  }
  double t1 = cur_time();
  printf("%ld primes in [%ld,%ld)\n", s, a, b);
  printf("%f sec\n", t1 - t0);
  return 0;
}
