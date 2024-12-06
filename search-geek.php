<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeeksForGeeks Search</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --primary-hover: #1d4ed8;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
        }

        .container {
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1rem;
            background: linear-gradient(90deg, #2563eb, #4f46e5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .description {
            color: var(--text-secondary);
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }

        .search-form {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .search-input {
            flex: 1;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            border: 2px solid var(--border-color);
            border-radius: 0.5rem;
            transition: border-color 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .search-button {
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            color: white;
            background-color: var(--primary-color);
            border: none;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .search-button:hover {
            background-color: var(--primary-hover);
        }

        .results {
            margin-top: 2rem;
        }

        .results h2 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .results ol {
            list-style-position: inside;
            padding-left: 0;
        }

        .results li {
            margin-bottom: 1rem;
            padding: 1rem;
            background: var(--card-bg);
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }

        .results li:hover {
            transform: translateY(-2px);
        }

        .results a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
        }

        .results a:hover {
            text-decoration: underline;
        }

        .recommendations {
            margin-top: 3rem;
            padding: 1.5rem;
            background: var(--card-bg);
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .recommendations h3 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .recommendations ul {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .recommendations li a {
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: #f1f5f9;
            border-radius: 2rem;
            color: var(--text-primary);
            text-decoration: none;
            transition: background-color 0.2s;
        }

        .recommendations li a:hover {
            background-color: #e2e8f0;
        }

        @media (max-width: 640px) {
            .search-form {
                flex-direction: column;
            }

            .search-button {
                width: 100%;
            }

            .container {
                margin: 1rem auto;
            }

            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
            <div class="header">
                <h1>GeeksForGeeks Search</h1>
                <p class="description">
                    Explore articles and resources from <a href="https://www.geeksforgeeks.org/" target="_blank">GeeksForGeeks</a>.
                    Try searching for topics like <strong>algorithms</strong>, <strong>data structures</strong>, or <strong>programming languages</strong>.
                </p>
            </div>
            <form action="search-geek.php" method="get" class="search-form">
                <input type="text" 
                       class="search-input"
                       name="search_string" 
                       value="<?php echo isset($_GET['search_string']) ? htmlspecialchars($_GET['search_string'], ENT_QUOTES) : ''; ?>" 
                       placeholder="Enter a query" />
                <button type="submit" class="search-button">Search</button>
            </form>
            <div class="results">
                <?php
                if (isset($_GET["search_string"])) {
                    $search_string = $_GET["search_string"];
                    file_put_contents("newlogs.txt", $search_string . PHP_EOL, FILE_APPEND | LOCK_EX);

                    $qfile = fopen("query.py", "w");
                    fwrite($qfile, "import pyterrier as pt\nif not pt.started():\n\tpt.init()\n\n");
                    fwrite($qfile, "import pandas as pd\nqueries = pd.DataFrame([[\"q1\", \"$search_string\"]], columns=[\"qid\",\"query\"])\n");
                    fwrite($qfile, "index = pt.IndexFactory.of(\"./geek_index/\")\n");
                    fwrite($qfile, "bm25 = pt.BatchRetrieve(index, wmodel=\"BM25\")\n");
                    fwrite($qfile, "results = bm25.transform(queries)\n");

                    for ($i = 0; $i < 5; $i++) {
                        fwrite($qfile, "print(index.getMetaIndex().getItem(\"filename\",results.docid[$i]))\n");
                        fwrite($qfile, "if index.getMetaIndex().getItem(\"title\", results.docid[$i]).strip() != \"\":\n");
                        fwrite($qfile, "\tprint(index.getMetaIndex().getItem(\"title\",results.docid[$i]))\n");
                        fwrite($qfile, "else:\n\tprint(index.getMetaIndex().getItem(\"filename\",results.docid[$i]))\n");
                    }
                    fclose($qfile);

                    exec("ls | nc -u 127.0.0.1 10024");
                    sleep(3);

                    $stream = fopen("output", "r");
                    $line = fgets($stream);

                    echo "<h2>Search Results</h2><ol>";
                    while (($line = fgets($stream)) != false) {
                        $clean_line = preg_replace('/\s+/', ',', $line);
                        $record = explode('/', $clean_line);
                        $line = fgets($stream);
                        echo "<li><a href=\"http://geeksforgeeks.org/$record[2]\">http://geeksforgeeks.org/$record[2]</a></li>";
                    }
                    echo "</ol>";
                    fclose($stream);
                    exec("rm query.py");
                    exec("rm output");
                }
                ?>
            </div>
        </div>
        <div class="recommendations">
            <h3>Recommendations</h3>
            <ul>
                <?php
                exec("sort newlogs.txt | uniq -c | sort -bgr | awk '{print $2}'", $output);
                $top3 = array_slice($output, 0, 3);
                foreach ($top3 as &$query) {
                    echo "<li><a href='?search_string=" . urlencode($query) . "'>$query</a></li>";
                }
                ?>
            </ul>
        </div>
    </div>
</body>
</html>