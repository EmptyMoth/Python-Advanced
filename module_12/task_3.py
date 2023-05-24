from threading import Semaphore, Thread
import time
import sys

sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
    print(1)
    sem.release()
    time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
    print(2)
    sem.release()
    time.sleep(0.25)


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)
thread_input: Thread = Thread(target=sys.stdin.readline)
threads: list[Thread] = [t1, t2, thread_input]
try:
    t1.daemon = True
    t2.daemon = True
    for thread in threads:
        thread.start()
    thread_input.join()
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    for thread in threads:
        thread.join(0)
    exit(1)
