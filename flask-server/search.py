from flask import Flask
import pandas as pd
import pyterrier as pt

app = Flask(__name__)
@app.route("/search")

def search():
    pt.java.set_java_home("C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.4.101-hotspot")
    queries = pd.DataFrame([["q1","python"], ["q2","nlp"]], columns=["qid","query"])
    index = pt.IndexFactory.of("C:\\Users\\vvaib\Documents\\Info376\\G4GSearchRecSys\\data\\geek_index\\data.properties")
    bm_25 = pt.BatchRetrieve(index, wmodel="BM25")

    # Create search query DataFrame
    # Load the index and perform search
    results = bm_25.transform(queries)
    print(results)
    results.to_csv()
    # index = pt.IndexFactory.of("./pg_index/data.properties")
    # tf_idf = pt.BatchRetrieve(index, wmodel="TF_IDF")
    # tf_idf.transform(queries)

    search_results = []
    for i in range(min(5, len(results))):
        filename = index.getMetaIndex().getItem("filename", results.docid[i])
        title = index.getMetaIndex().getItem("title", results.docid[i]).strip()
        if not title:
            title = filename

        url = f"https://{filename.replace('./', '')}"
        search_results.append({"url": url, "title": title})


    return search_results
    # print(index.getMetaIndex().getKeys())
    # print(index.getMetaIndex().getItem("filename", 15))
    # print(index.getMetaIndex().getItem("title", 15))

if __name__ == "__main__":
    app.run(debug=True)