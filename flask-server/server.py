from flask import Flask
import pandas as pd 
import pyterrier as pt 

app = Flask(__name__)
@app.route("/search")

def search():
    #Change to your JDK path
    pt.java.set_java_home("C:\\Users\\Amrith\\.jdks\\temurin-11.0.16.1")
    if not pt.started():
        pt.java.init()
    return str(pt.java.started())
  
  
if __name__ == "__main__":
    app.run(debug=True)