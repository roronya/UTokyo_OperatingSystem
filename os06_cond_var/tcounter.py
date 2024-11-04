import sys
import threading
import time

class scounter:
    """
    飽和カウンタ
    """
    def __init__(self, capacity):
        self.x = 0
        self.capacity = capacity
        self.m = threading.Lock()
        self.c = [threading.Condition(self.m), threading.Condition(self.m)]
    def inc(self):
        self.m.acquire()
        x = None
        while True:
            x = self.x
            if x < self.capacity:
                break
            self.c[0].wait()
        x = self.x
        self.x = x + 1
        if x == 0:
            self.c[1].notify_all()
        self.m.release()
        return x
    def dec(self):
        self.m.acquire()
        x = None
        while True:
            x = self.x
            if x > 0:
                break
            self.c[1].wait()
        x = self.x
        self.x = x - 1
        if x == self.capacity:
            self.c[0].notify_all()
        self.m.release()
        return x
    def get(self):
        return self.x

def main():
    argv = sys.argv
    # incを呼ぶスレッド数 
    n_inc_threads = int(argv[1]) if 1 < len(argv) else 3
    # decを呼ぶスレッド数 
    n_dec_threads = int(argv[2]) if 2 < len(argv) else 2
    # incとdecが呼ばれる回数(全スレッドの合計)
    n             = int(argv[3]) if 3 < len(argv) else 10000
    # 飽和する値
    capacity      = int(argv[4]) if 4 < len(argv) else 10000
    s = scounter(capacity)
    print(f"increment threads : {n_inc_threads}")
    print(f"decrement threads : {n_dec_threads}")
    print(f"increments/decrements : {n}")
    print(f"capacity : {capacity}")
    def inc_thread_fun(idx):
        # increment
        a = n *  idx      // n_inc_threads
        b = n * (idx + 1) // n_inc_threads
        for i in range(a, b):
            x = s.inc()
            assert(x < capacity), (x, capacity)
            assert(x >= 0), x
    def dec_thread_fun(idx):
        a = n *  idx      // n_dec_threads;
        b = n * (idx + 1) // n_dec_threads;
        for i in range(a, b):
            x = s.dec()
            assert(x <= capacity), (x, capacity)
            assert(x > 0), x
    inc_threads = [threading.Thread(target=inc_thread_fun, args=(i,)) for i in range(n_inc_threads)]
    dec_threads = [threading.Thread(target=dec_thread_fun, args=(i,)) for i in range(n_dec_threads)]
    t0 = time.time()
    for th in inc_threads + dec_threads:
        th.start()
    for th in inc_threads + dec_threads:
        th.join()
    t1 = time.time()
    dt = t1 - t0
    print(f"took {dt:.9f} sec")
    x = s.get()
    ok_ng = "OK" if x == 0 else "NG"
    print(f"{ok_ng} : value at the end = {x}")
    return x != 0
    
sys.exit(main())
