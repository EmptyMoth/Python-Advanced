import os
import re
import random
from flask import Flask


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, "war_and_peace.txt")

app = Flask(__name__)


@app.route('/get_random_word')
def get_random_word_from_war_and_peace():
    return random.choice(_all_words_from_war_and_peace)


def _write_all_words(file: str) -> [str]:
    with open(file, encoding="utf-8") as book:
        return re.findall(r"\b\w+\b", book.read())


_all_words_from_war_and_peace: [str] = _write_all_words(BOOK_FILE)


if __name__ == "__main__":
    app.run()
