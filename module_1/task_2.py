from flask import Flask


app = Flask(__name__)

cars: [str] = ["Chevrolet", "Renault", "Ford", "Lada"]


@app.route("/cars")
def list_cars():
    return str(cars)


if __name__ == "__main__":
    app.run()
