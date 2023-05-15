import task_1_orm as orm
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask("library")


@app.before_request
def before_request():
    orm.create_metadata()


# @app.route("/", methods=["GET"])
# def add():
#     orm.session.add(orm.Authors(id=1, name="Hermann", surname="Hesse"))
#     orm.session.commit()
#     return "OK"


@app.route("/library/all_books", methods=["GET"])
def get_all_books():
    books = orm.session.query(orm.Books).all()
    books_list: list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


@app.route("/library/debtors", methods=["GET"])
def get_all_debtors():
    debtors = orm.session.query(orm.Students) \
        .outerjoin(orm.ReceivingBooks, orm.ReceivingBooks.student_id == orm.Students.id) \
        .filter(orm.ReceivingBooks.count_date_with_book > 14).all()
    debtors_list: list = [debtor.to_json() for debtor in debtors]
    return jsonify(debtors_list=debtors_list), 200


@app.route("/library/issue_book", methods=["POST"])
def give_book_to_student():
    book_id = request.form.get("book_id", type=int)
    student_id = request.form.get("student_id", type=int)
    new_receiving_books = orm.ReceivingBooks(book_id=book_id,
                                             student_id=student_id,
                                             date_of_issue=datetime.now())
    orm.session.add(new_receiving_books)
    orm.session.commit()
    return "Книга выдана", 201


@app.route("/library/return_book", methods=["POST"])
def return_book_from_student():
    book_id = request.form.get("book_id", type=int)
    student_id = request.form.get("student_id", type=int)
    try:
        query = orm.session.query(orm.ReceivingBooks) \
            .filter(orm.ReceivingBooks.book_id == book_id, orm.ReceivingBooks.student_id == student_id) \
            .order_by(orm.ReceivingBooks.date_of_return.desc()) \
            .first()
        query.date_of_return = datetime.now()
        orm.session.commit()
        return "Книга возвращена", 200
    except Exception as exp:
        return f"Такой записи нет \nLOG: {exp}", 404


@app.route("/library/get_book/<key_string>", methods=["GET"])
def get_book(key_string: str):
    books = orm.session.query(orm.Books) \
        .filter(orm.Books.name.like(f"%{key_string}%")).all()
    books_list: list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


if __name__ == '__main__':
    app.run(debug=True)
