import os
import sys
import time

def cur_time():
    return int(time.time() * 1.0e9)

def main():
    n = int(sys.argv[1]) if 1 < len(sys.argv) else 5
    t0 = cur_time()

    for i in range(n):
        pid = os.fork()
        if pid == 0:
            argv = ["./do_nothing"]
            os.execv(argv[0], argv)
            sys.exit()
        else:
            os.waitpid(pid, 0)
  
    t1 = cur_time()
    dt = t1 - t0
    print(f"{dt} nsec to fork-exec-wait {n} processes ({dt / n} nsec/proc)")

main()
