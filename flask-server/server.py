from flask import Flask

app = Flask(__name__)
@app.route("/search")
def search():
    return("search system")

if __name__ == "__main__":
    app.run(debug=True)