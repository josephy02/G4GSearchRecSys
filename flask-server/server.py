from flask import Flask

app = Flask(__name__)
@app.route("/search")

def search():
    #Change to your JDK path
    return "hello"




if __name__ == "__main__":
    app.run(debug=True)