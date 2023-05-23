import logging
import random
import time

from threading import Thread, Event, Semaphore


SELLER_COUNT: int = 3
SEATS_COUNT: int = 20
TOTAL_TICKETS: int = 10
TICKETS_COUNT: int = TOTAL_TICKETS

on_tickets_running_out: Event = Event()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Worker(Thread):
    def __init__(self, semaphore: Semaphore) -> None:
        super().__init__()
        self.semaphore: Semaphore = semaphore
        logger.info(f'{self.__class__.__name__} started work')

    @staticmethod
    def perform_work():
        time.sleep(random.randint(0, 1))


class Director(Worker):
    on_printed_is_place: Event = Event()

    def __init__(self, semaphore: Semaphore) -> None:
        super().__init__(semaphore)
        self.printed_tickets: int = 0
        Director.on_printed_is_place.set()

    def run(self) -> None:
        global TOTAL_TICKETS, SELLER_COUNT, SEATS_COUNT
        while True:
            on_tickets_running_out.wait()
            with self.semaphore:
                if TOTAL_TICKETS > SEATS_COUNT:
                    break

                Director.on_printed_is_place.clear()
                Worker.perform_work()
                self._print_tickets(2 * SELLER_COUNT)
                Director.on_printed_is_place.set()
                on_tickets_running_out.clear()
                logger.info(f'{self.name} printed one;  {TOTAL_TICKETS} left')

        logger.info(f'Director {self.name} printed {self.printed_tickets} tickets')

    def _print_tickets(self, printed_tickets: int) -> None:
        global TOTAL_TICKETS, TICKETS_COUNT
        self.printed_tickets += printed_tickets
        TOTAL_TICKETS += printed_tickets
        TICKETS_COUNT += printed_tickets


class Seller(Worker):
    def __init__(self, semaphore: Semaphore) -> None:
        super().__init__(semaphore)
        self.tickets_sold: int = 0

    def run(self) -> None:
        global TICKETS_COUNT
        while True:
            Worker.perform_work()
            Director.on_printed_is_place.wait()
            with self.semaphore:
                if TICKETS_COUNT <= 0:
                    break

                self._sell_tickets(1)
                logger.info(f'{self.name} sold one;  {TICKETS_COUNT} left')

        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def _sell_tickets(self, tickets_sold: int) -> None:
        global TICKETS_COUNT
        self.tickets_sold += tickets_sold
        TICKETS_COUNT -= tickets_sold
        if TICKETS_COUNT < 2 * SEATS_COUNT:
            on_tickets_running_out.set()


if __name__ == '__main__':
    semaphore: Semaphore = Semaphore()
    director: Director = Director(semaphore)
    sellers: [Seller] = [Seller(semaphore) for _ in range(SELLER_COUNT)]

    director.start()
    for seller in sellers:
        seller.start()

    director.join()
    for seller in sellers:
        seller.join()
