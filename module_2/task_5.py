from flask import Flask


app = Flask(__name__)


@app.route("/max_number/<path:numbers_path>")
def get_max_number(numbers_path: str) -> str:
    numbers_str: [str] = numbers_path.split('/')
    max_number: int = max(map(int, filter(lambda x: x.isdigit(), numbers_str)))
    return f"Максимальное число: <i>{max_number}</i>"


if __name__ == "__main__":
    app.run(debug=True)
