import requests
import time
import multiprocessing

from multiprocessing.pool import ThreadPool
from threading import Thread
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine("sqlite:///task_1.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

MAIN_URL: str = "https://swapi.dev/api/"
URL_WITH_PEOPLE: str = "".join([MAIN_URL, "people/{}/"])
PEOPLE_COUNT: int = 25


class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(String, nullable=True)
    gender = Column(String, nullable=True)

    def __repr__(self):
        return f"name = {self.name}, birth_year = {self.birth_year}, gender = {self.gender}"


def explore_people_with_threadpool() -> None:
    start_time: time = time.time()
    pool = ThreadPool(processes=PEOPLE_COUNT)
    pool.map(_explore_people, range(1, PEOPLE_COUNT + 1))
    pool.close()
    pool.join()
    end_time: time = time.time() - start_time
    print("explore_people_with_threadpool", end_time)


def explore_people_with_processpool() -> None:
    start_time: time = time.time()
    pool = multiprocessing.Pool()
    pool.map(_explore_people, range(1, PEOPLE_COUNT + 1))
    pool.close()
    pool.join()
    end_time: time = time.time() - start_time
    print("explore_people_with_processpool", end_time)


def _explore_people(people_number: int) -> None:
    information: dict | None = _get_information(URL_WITH_PEOPLE.format(people_number))
    if information is None:
        return

    people = People(name=information["name"], birth_year=information["birth_year"], gender=information["gender"])
    session.add(people)


def _get_information(url: str) -> dict | None:
    response = requests.get(url, timeout=5)
    return response.json() if response.status_code == 200 else None


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    explore_people_with_threadpool()
    explore_people_with_processpool()
    session.commit()
