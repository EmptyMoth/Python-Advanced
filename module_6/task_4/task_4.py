@app.route()
def hello_world():
    with open("hello_world.html", 'r') as file:
        return file.read()