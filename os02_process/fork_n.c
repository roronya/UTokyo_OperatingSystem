#include <stdio.h>
#include <unistd.h>

int main() {
  int n = 1;
  for (int i = 0; i < n; i++) {
    pid_t cid = fork();
    printf("%d -> %d: %d\n", getpid(), cid, i);
    fflush(stdout);
  }
  return 0;
}
