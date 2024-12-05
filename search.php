<html>
<head>
      	<title>My Search</title>
</head>

<body>

<h1>My Search</h1>
<p>Here's a UI that searches through an index of documents from web crawling on the Allen Institute's official $
<p>Given that the Allen Institute is famous for its groundbreaking research, some interesting queries to try ar$
<form action="search.php" method="post">
        <input type="text" size=40 name="search_string" value="<?php echo $_POST["search_string"];?>"/>
        <input type="submit" value="Search"/>
</form>

<?php
     	if (isset($_POST["search_string"])) {
                $search_string = $_POST["search_string"];

                file_put_contents("logs.txt", $search_string.PHP_EOL, FILE_APPEND | LOCK_EX);

                $qfile = fopen("query.py", "w");
                fwrite($qfile, "import pyterrier as pt\nif not pt.started():\n\tpt.init()\n\n");
                fwrite($qfile, "import pandas as pd\nqueries = pd.DataFrame([[\"q1\", \"$search_string\"]], col$
                fwrite($qfile, "index = pt.IndexFactory.of(\"./ai_index/\")\n");
                fwrite($qfile, "tf_idf = pt.BatchRetrieve(index, wmodel=\"BM25\")\n");
                fwrite($qfile, "results = tf_idf.transform(queries)\n");

                for ($i=0; $i<5; $i++) {
                        fwrite($qfile, "print(index.getMetaIndex().getItem(\"filename\",results.docid[$i]))\n");
                        fwrite($qfile, "if index.getMetaIndex().getItem(\"title\", results.docid[$i]).strip() !$
                        fwrite($qfile, "\tprint(index.getMetaIndex().getItem(\"title\",results.docid[$i]))\n");
                        fwrite($qfile, "else:\n\tprint(index.getMetaIndex().getItem(\"filename\",results.docid[$
                }
                fclose($qfile);

                exec("ls | nc -u 127.0.0.1 10019");
                sleep(3);

                $stream = fopen("output", "r");

                $line=fgets($stream);

                while(($line=fgets($stream))!=false) {
                        $clean_line = preg_replace('/\s+/',',',$line);
                        $record = explode("./", $clean_line);
                        $line = fgets($stream);
                        echo "<a href=\"http://$record[1]\">".$line."</a><br/>\n";
                }

                fclose($stream);

                exec("rm query.py");
                exec("rm output");
                }
?>
</body>
</html>
