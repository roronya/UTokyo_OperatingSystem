#define _GNU_SOURCE
#include <assert.h>
#include <sched.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


/* 時刻 begin -- end まで proc 上で動いていた記録 */
typedef struct {
  double begin;
  double end;
  int proc;
} rec_t;

/* 現在時刻を得る */
double cur_time() {
  struct timeval tp[1];
  gettimeofday(tp, 0);
  return tp->tv_sec + tp->tv_usec * 1.0E-6;
}

/* T秒間走り続け, CPUが割り当てられていたと思しき時間帯を記録する */
int run(double T, int n) {
  pid_t pid = getpid();
  double limit = cur_time() + T;
  rec_t * R = (rec_t *)calloc(n, sizeof(rec_t));
  int i = 0;
  R[i].begin = R[i].end = cur_time();
  R[i].proc = sched_getcpu();

  while (R[i].end < limit && i < n) {
    double t = cur_time(); /* 現在時刻を得る */
    int proc = sched_getcpu();
    if (t - R[i].end < 1.0E-3 && proc == R[i].proc) {
      /* 最後に見た時刻とあまり変わらない(< 1ms) -> R[i].endを増やす */
      R[i].end = t;
    } else {
      /* 最後に見た時刻から1ms以上たっている -> 新しい区間に入る */
      if (i + 1 >= n) break;
      i++;
      R[i].proc = proc;
      R[i].begin = R[i].end = cur_time();
    }
  }
  assert(i < n);
  int j;
  for (j = 0; j <= i; j++) {
    printf("%d %f %f %d %f\n", 
           pid, R[j].begin, R[j].end, R[j].proc,
           R[j].end - R[j].begin);
  }
  return 0;
}


int main(int argc, char ** argv) {
  double T = (argc > 1 ? atof(argv[1]) : 10.0);
  int n    = (argc > 2 ? atoi(argv[2]) : 100000);

  run(T, n);
  return 0;
}
