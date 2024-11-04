
import sys
import threading
import time

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

def parallel_for(f, a, b, nthreads):
    """
    #pragma omp parallel for に似たもの
    f(a), f(a+1), ..., f(b-1) を nthreads で分割して実行
    """
    def thread_fun(i):
        ai = (a * (nthreads - i)     + b * i) // nthreads
        bi = (a * (nthreads - i - 1) + b * (i + 1)) // nthreads
        for i in range(ai, bi):
            f(i)
    parallel(thread_fun, nthreads)

class bounded_buffer:
    """
    有限バッファ
    要素は必ず >= 0 とする
    """
    def __init__(self, capacity):
        self.a = [0] * capacity
        self.capacity = capacity
        self.n_gets = 0
        self.n_puts = 0
    def put(self, x):
        """
        要素を追加 
        満杯だったら待つようにするのが課題
        以下はそのままだと満杯の場合は0を返す(間違い)
        """
        g = self.n_gets
        p = self.n_puts
        cap = self.capacity
        assert(x >= 0), x
        if p - g >= cap:
            return 0 # NG
        self.a[p % cap] = x
        self.n_puts = p + 1
        return 1 # OK
    def get(self):
        """
        要素を取り出す
        空だったら待つようにするのが課題
        以下はそのままだと空の場合は-1を返す(間違い)
        """
        g = self.n_gets
        p = self.n_puts
        cap = self.capacity
        if p - g <= 0:
            return -1 # 空 
        x = self.a[g % cap]
        self.n_gets = g + 1
        assert(x >= 0), x
        return x

def main():
    i = 1
    argv = sys.argv
    argc = len(argv)
    # putするスレッド数
    n_putter_threads = int(argv[i]) if i < argc else 1
    i += 1
    # getするスレッド数 
    n_getter_threads = int(argv[i]) if i < argc else 1
    i += 1
    # putとgetの間にbarrierを入れるか?
    barrier_between_puts_gets = int(argv[i]) if i < argc else 1
    i += 1
    # put (get)される回数
    n                = int(argv[i]) if i < argc else 1000000
    i += 1
    # 容量
    capacity         = int(argv[i]) if i < argc else 1000
    i += 1
    # 検証用(validate[x] == 1 iff getでxが取り出された)
    validate = [0] * n
    bb = bounded_buffer(capacity)
    nthreads = n_putter_threads + n_getter_threads
    barrier = threading.Barrier(nthreads)

    def thread_fun(idx):
        if idx < n_putter_threads:
            # I am a putter thread
            a = n *  idx      // n_putter_threads
            b = n * (idx + 1) // n_putter_threads
            # 0,1,...,n-1 を1つずつput
            for x in range(a, b):
                ok = bb.put(x)
                assert(ok)
            if barrier_between_puts_gets:
                # putが全員終わってからget
                barrier.wait()
        else:
            idx -= n_putter_threads
            # I am a getter thread
            a = n *  idx      // n_getter_threads
            b = n * (idx + 1) // n_getter_threads
            # 0,1,...,n-1 を1つずつget
            if barrier_between_puts_gets:
                # putが全員終わってからget
                barrier.wait()
            for i in range(a, b):
                x = bb.get()
                assert(x >= 0), x
                assert(x < n), x
                assert(validate[x] == 0), validate[x]
                validate[x] = 1
    t0 = time.time()
    parallel(thread_fun, nthreads)
    t1 = time.time()
    dt = t1 - t0
    print(f"{dt} sec")
    for i in range(n):
        assert(validate[i] == 1), validate[i]
    print("OK")
    return 0

sys.exit(main())
