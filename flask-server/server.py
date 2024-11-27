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

def index(): 
    files = pt.io.find_files("/data")
    indexer = pt.FilesIndexer("/data/g4g_index",
                            meta={"docno":20,"filename":1024,"title":1024},meta_tags={"title":"title"})
    indexref = indexer.index(files)
    index = pt.IndexFactory.of(indexref)
    
def model():
    queries = pd.DataFrame([["q1","python"], ["q2","nlp"]], columns=["qid","sql"])
    index = pt.IndexFactory.of("./g4g_index_index/data.properties")
    bm_25 = pt.BatchRetrieve(index, wmodel="BM_25")
    bm_25.transform(queries)



if __name__ == "__main__":
    app.run(debug=True)