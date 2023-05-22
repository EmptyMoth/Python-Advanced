from sqlalchemy import create_engine, Column, \
    Integer, Text, Date, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta


engine = create_engine("sqlite:///task_1.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)

    def __repr__(self):
        return f"{self.name} {self.surname}"

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def get_students_from_dormitories(cls):
        return session.query(Students).filter(Students.scholarship).all()

    @classmethod
    def get_students_with_higher_average_score(cls, average_score: float):
        return session.query(Students).filter(Students.average_score > average_score).all()

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReceivingBooks(Base):
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False, default=datetime.now)
    date_of_return = Column(DateTime, nullable=True)

    @hybrid_property
    def count_date_with_book(self) -> int:
        dates = session.query(ReceivingBooks.date_of_issue, ReceivingBooks.date_of_return) \
            .filter(ReceivingBooks.date_of_issue == self.date_of_issue,
                    ReceivingBooks.date_of_return == self.date_of_return).first()
        date_of_issue, date_of_return = dates

        date_final: datetime = date_of_return if date_of_return is not None else datetime.now()
        time_with_book = date_final - date_of_issue
        return time_with_book.days

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create_metadata() -> None:
    Base.metadata.create_all(bind=engine)
