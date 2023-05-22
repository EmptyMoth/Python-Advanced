import re
from sqlalchemy import create_engine, event, func, Column, \
    Integer, Text, Date, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

engine = create_engine("sqlite:///task_1.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)

    def __init__(self, name: str, surname: str) -> None:
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f"{self.name} {self.surname}"

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey(f"{Author.__tablename__}.id"), nullable=False)

    author = relationship(Author.__name__, backref=backref(__tablename__,
                                                           cascade="all, delete-orphan",
                                                           lazy="joined"))

    receiving_books = relationship("ReceivingBook",
                                   back_populates="book", cascade="all, delete-orphan", lazy="joined")
    students = association_proxy("receiving_books", "student")

    def __init__(self, name: str, release_date: datetime, count: int = 1) -> None:
        self.name = name
        self.count = count
        self.release_date = release_date

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    receiving_books = relationship("ReceivingBook",
                                   back_populates="student", cascade="all, delete-orphan", lazy="joined")
    books = association_proxy("receiving_books", "book")

    def __init__(self, name: str, surname: str,
                 phone: str, email: str, average_score: float, scholarship: bool) -> None:
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.average_score = average_score
        self.scholarship = scholarship

    @classmethod
    def get_students_from_dormitories(cls):
        return session.query(Student).filter(Student.scholarship).all()

    @classmethod
    def get_students_with_higher_average_score(cls, average_score: float):
        return session.query(Student).filter(Student.average_score > average_score).all()

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReceivingBook(Base):
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey(f"{Book.__tablename__}.id"), nullable=False)
    student_id = Column(Integer, ForeignKey(f"{Student.__tablename__}.id"), nullable=False)
    date_of_issue = Column(DateTime, nullable=False, default=datetime.now)
    date_of_return = Column(DateTime, nullable=True)

    book = relationship(Book.__name__, back_populates="receiving_books")
    student = relationship(Student.__name__, back_populates="receiving_books")

    def __init__(self, book_id: int, student_id: int,
                 date_of_issue: datetime, date_of_return: datetime = None) -> None:
        self.book_id = book_id
        self.student_id = student_id
        self.date_of_issue = date_of_issue
        self.date_of_return = date_of_return

    @hybrid_property
    def count_date_with_book(self) -> int:
        dates = session.query(ReceivingBook.date_of_issue, ReceivingBook.date_of_return) \
            .filter(ReceivingBook.date_of_issue == self.date_of_issue,
                    ReceivingBook.date_of_return == self.date_of_return).first()

        date_of_issue, date_of_return = dates
        date_final: datetime = date_of_return if date_of_return is not None else datetime.now()
        time_with_book = date_final - date_of_issue
        return time_with_book.days

    def to_json(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create_metadata() -> None:
    Base.metadata.create_all(bind=engine)


@event.listens_for(session, 'before_attach')
def receive_before_attach(session, object):
    if type(object) is not Student:
        return

    phone = re.match(r"^\+7\(9\d\d\)-\d\d\d-\d\d-\d\d$", object.phone)
    if phone is None:
        object.phone = ""
