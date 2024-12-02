import pandas as pd
import pyterrier as pt

def main():
    # pt.java.set_java_home("C:\\Users\\Amrith\\.jdks\\temurin-11.0.16.1")
    queries = pd.DataFrame([["q1","python"], ["q2","nlp"]], columns=["qid","query"])
    # index = pt.IndexFactory.of("C:\\Users\\Amrith\\Documents\\info376\\G4GSearchRecSys\\data\\geek_index\\data.properties")
    index = pt.IndexFactory.of("./data/geek_index/data.properties")
    bm_25 = pt.BatchRetrieve(index, wmodel="BM25")

    # Create search query DataFrame
    # Load the index and perform search
    results = bm_25.transform(queries)
    print(results)
    results.to_csv()
    # index = pt.IndexFactory.of("./pg_index/data.properties")
    # tf_idf = pt.BatchRetrieve(index, wmodel="TF_IDF")
    # tf_idf.transform(queries)

    # Process results
    search_results = []
    for i in range(min(10, len(results))):
        filename = index.getMetaIndex().getItem("filename", results.docid[i])
        title = index.getMetaIndex().getItem("title", results.docid[i]).strip()
        if not title:
            title = filename

        url = f"https://{filename.replace('./', '')}"
        search_results.append({"url": url, "title": title})


    print(search_results)
    # print(index.getMetaIndex().getKeys())
    # print(index.getMetaIndex().getItem("filename", 15))
    # print(index.getMetaIndex().getItem("title", 15))

if __name__ == "__main__":
    main()


