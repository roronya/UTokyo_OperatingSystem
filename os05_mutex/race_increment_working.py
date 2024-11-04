import random
import sys
import threading
g = 0

def parallel(f, nthreads):
    """
    #pragma omp parallel に似たもの

    f(0), f(1), ..., f(nthreads - 1) の各々をスレッドで実行
    """
    threads = [threading.Thread(target=f, args=(i, ))
               for i in range(nthreads)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

def main():
    global g
    argv = sys.argv
    argc = len(argv)
    i = 1
    n = int(argv[i]) if i < argc else 1000000
    i += 1
    nthreads = int(argv[i]) if i < argc else 2
    i += 1

    g = 0
    def thread_fun(idx):
        global g
        for i in range(n):
            g += 1
    parallel(thread_fun, nthreads)
    print(f"g = {g}")
    return 0

sys.exit(main())
