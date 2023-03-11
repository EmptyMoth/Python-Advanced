import random
from flask import Flask


app = Flask(__name__)

_cats: [str] = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]


@app.route('/cats')
def random_cat():
    return random.choice(_cats)


if __name__ == "__main__":
    app.run()
