from flask import Flask
from datetime import datetime


app = Flask(__name__)


_WEEK_DAYS: tuple = ("понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья")


@app.route("/hello-world/<name>")
def hello_world(name: str) -> str:
    day_phrase: str = _get_day_phrase()
    return f"Привет, {name.capitalize()}. {day_phrase}!"


# Не лучше ли использовать match, чем хранить кортеж?
def _get_day_phrase() -> str:
    week_day_number: int = datetime.today().weekday()
    week_day: str = _WEEK_DAYS[week_day_number]
    match week_day_number:
        case 2 | 4 | 5:
            return ' '.join(["Хорошей", week_day])
        case _:
            return ' '.join(["Хорошего", week_day])


if __name__ == "__main__":
    app.run(debug=True)
