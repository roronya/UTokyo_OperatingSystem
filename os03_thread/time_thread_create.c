/* 必要な #include を補うこと (man ページを参照) */
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

long cur_time() {
  struct timespec ts[1];
  clock_gettime(CLOCK_REALTIME, ts);
  return ts->tv_sec * 1000000000L + ts->tv_nsec;
}

void * do_nothing(void * arg) {
  /**
  pthread_t my_thread_id = pthread_self();  
  printf("thread_id: %lu\n", my_thread_id);
  **/
  return arg;
}

int main(int argc, char ** argv) {
  int n = (argc > 1 ? atoi(argv[1]) : 5);
  long t0 = cur_time();
  pthread_t child_thread_id;

  for (int i=0;i<n;i++) {    
    if (pthread_create(&child_thread_id, 0, do_nothing, 0)) {
      err(1, "pthread_create");
    }
    void * ret = 0;
    if (pthread_join(child_thread_id, &ret)) {
      err(1, "pthread_join");
    }
  }
  long t1 = cur_time();
  long dt = t1 - t0;
  printf("%ld nsec to pthrea_create-and-join %d threads (%ld nsec/thread)\n",
         dt, n, dt / n);
  return 0;
}
