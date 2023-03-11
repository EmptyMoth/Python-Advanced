from flask import Flask


app = Flask(__name__)


@app.route("/counter")
def counter():
    counter.visits += 1
    return str(counter.visits)


counter.visits = 0


if __name__ == "__main__":
    app.run()
