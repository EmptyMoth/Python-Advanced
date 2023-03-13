import os
from flask import Flask


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/preview/<int:size>/<path:relative_path>")
def preview_file(size: int, relative_path: str) -> str:
    abs_path: str = _get_abs_path(relative_path)
    with open(abs_path) as file:
        text: str = file.read(size)
        return f"<b>{abs_path}</b> {len(text)}<br>{text}"


def _get_abs_path(path: str) -> str:
    return os.path.join(BASE_DIR, path)


if __name__ == "__main__":
    app.run(debug=True)
