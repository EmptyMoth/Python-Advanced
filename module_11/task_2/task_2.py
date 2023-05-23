import requests
import json
import time

from threading import Thread
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine("sqlite:///task_2.db")
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


def explore_people_sequentially() -> None:
    start_time: time = time.time()
    for i in range(1, PEOPLE_COUNT + 1):
        _explore_people(i)

    end_time: time = time.time() - start_time
    print("explore_people_sequentially", end_time)


def explore_people_in_parallel() -> None:
    start_time: time = time.time()
    threads: [Thread] = [Thread(target=_explore_people, args=[i + 1]) for i in range(PEOPLE_COUNT)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time: time = time.time() - start_time
    print("explore_people_in_parallel", end_time)


def _explore_people(people_number: int) -> None:
    content: bytes | None = _get_content(URL_WITH_PEOPLE.format(people_number))
    if content is None:
        return

    information: dict = json.loads(content)
    people = People(name=information["name"], birth_year=information["birth_year"], gender=information["gender"])
    session.add(people)


def _get_content(url: str) -> bytes | None:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.content


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    explore_people_sequentially()
    explore_people_in_parallel()
    session.commit()
