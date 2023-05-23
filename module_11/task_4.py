import random
import time

from threading import Thread
from queue import PriorityQueue


class Producer(Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__()
        self.queue: PriorityQueue = queue
        print("Producer: Running")

    def run(self):
        priorities = range(10)
        for _ in range(10):
            priority: int = random.choice(priorities)
            task: tuple = (priority, time.sleep)
            self.queue.put(task)

        print("Producer: Done")


class Consumer(Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__()
        self.queue: PriorityQueue = queue
        print("Consumer: Running")

    def run(self):
        while not self.queue.empty():
            priority, task = self.queue.get()
            work_time: float = random.random()
            print(f">running Task(priority={priority}).\t{task.__name__}({work_time})")
            task(work_time)
            self.queue.task_done()

        print("Consumer: Done")


if __name__ == '__main__':
    queue: PriorityQueue = PriorityQueue()
    Producer(queue).start()
    Consumer(queue).start()

    queue.join()
