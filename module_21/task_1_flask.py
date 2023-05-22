import task_1_orm as db
import csv
from task_1_orm import Book, Student, Author, ReceivingBook
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask("library")


@app.before_request
def before_request():
    db.create_metadata()


# @app.route("/", methods=["GET"])
# def add():
#     db.session.add(db.Authors(id=1, name="Hermann", surname="Hesse"))
#     db.session.commit()
#     return "OK"


@app.route("/library/all_books", methods=["GET"])
def get_all_books():
    books = db.session.query(Book).all()
    books_list: list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


@app.route("/library/debtors", methods=["GET"])
def get_all_debtors():
    debtors = db.session.query(Student) \
        .outerjoin(ReceivingBook, ReceivingBook.student_id == Student.id) \
        .filter(ReceivingBook.count_date_with_book > 14).all()
    debtors_list: list = [debtor.to_json() for debtor in debtors]
    return jsonify(debtors_list=debtors_list), 200


@app.route("/library/issue_book", methods=["POST"])
def give_book_to_student():
    book_id = request.form.get("book_id", type=int)
    student_id = request.form.get("student_id", type=int)
    new_receiving_books = ReceivingBook(book_id, student_id, datetime.now())
    db.session.add(new_receiving_books)
    db.session.commit()
    return "Книга выдана", 201


@app.route("/library/return_book", methods=["POST"])
def return_book_from_student():
    book_id = request.form.get("book_id", type=int)
    student_id = request.form.get("student_id", type=int)
    try:
        query = db.session.query(ReceivingBook) \
            .filter(ReceivingBook.book_id == book_id, ReceivingBook.student_id == student_id) \
            .order_by(ReceivingBook.date_of_return.desc()) \
            .first()
        query.date_of_return = datetime.now()
        db.session.commit()
        return "Книга возвращена", 200
    except Exception as exp:
        return f"Такой записи нет \nLOG: {exp}", 404


@app.route("/library/get_book/<key_string>", methods=["GET"])
def get_book(key_string: str):
    books = db.session.query(db.Book) \
        .filter(Book.name.like(f"%{key_string}%")).all()
    books_list: list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


@app.route("/library/get_number_of_author_is_remaining_books/<int:author_id>", methods=["GET"])
def get_number_of_author_is_remaining_books(author_id: int):
    books_count = db.session.query(db.func.sum(Book.count)) \
        .filter(Book.author_id == author_id).scalar()
    return books_count, 200


@app.route("/library/get_books_list_student_not_read/<int:student_id>", methods=["GET"])
def get_books_list_student_not_read(student_id: int):
    student: Student = db.session.query(Student).filter(Student.id == student_id).scalar()
    books = map(lambda book: book.id, student.books)
    authors = db.session.query(Author).subquery()
    books_list = db.session.query(Book) \
        .join(authors, Book.author_id == authors.columns.id) \
        .group_by(authors.columns.id) \
        .filter(Book.id.not_in(books)).all()
    return books_list, 200


@app.route("/library/get_average_number_of_books_students_have_borrowed_current_month", methods=["GET"])
def get_average_number_of_books_students_have_borrowed_current_month():
    books_count = db.session.query(db.func.count(ReceivingBook.book_id)) \
        .group_by(ReceivingBook.student_id) \
        .filter(db.func.extract('month', ReceivingBook.date_of_issue) == datetime.now().month).subquery()
    books_count_average: float = db.session.query(db.func.avg(books_count)).scalar()
    return str(books_count_average), 200


@app.route("/library/get_most_popular_book_among_students_with_high_gpa", methods=["GET"])
def get_most_popular_book_among_students_with_high_gpa():
    gpa: float = 4.0
    books_count = db.session.query(Book.name.label("book"), db.func.count(ReceivingBook.student_id).label("count")) \
        .group_by(ReceivingBook.book_id) \
        .filter(Book.id == ReceivingBook.book_id, Student.id == ReceivingBook.student_id, Student.average_score > gpa) \
        .subquery()

    most_popular_book: str = \
        db.session.query(books_count.columns.book, db.func.max(books_count.columns.count)).scalar()
    return most_popular_book, 200


@app.route("/library/get_top_most_reading_students_this_year", methods=["GET"])
def get_top_most_reading_students_this_year():
    top_students = db.session.query(Student.name) \
        .group_by(ReceivingBook.student_id) \
        .filter(Student.id == ReceivingBook.student_id) \
        .order_by(db.func.count(ReceivingBook.book_id).desc()) \
        .limit(10) \
        .all()

    return str(top_students), 200


@app.route("/library/set_students_data", methods=["POST"])
def set_students_data():
    students_data = request.files["students_data"]
    with open(students_data.filename, mode='r') as file:
        reader = csv.DictReader(file, delimiter=";")
        students: [Student] = [{
            "name": row["name"],
            "surname": row["surname"],
            "phone": row["phone"],
            "email": row["email"],
            "average_score": float(row["average_score"]),
            "scholarship": bool(row["scholarship"])
            } for row in reader]

        db.session.bulk_insert_mappings(Student, students)
        db.session.commit()
    return "Succcess!", 200


if __name__ == '__main__':
    app.run(debug=True)
