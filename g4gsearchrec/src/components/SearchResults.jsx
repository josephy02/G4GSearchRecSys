import React from 'react';

const SearchResults = ({ results, onClick }) => {
    return (
        <div>
            <h2>Search Results</h2>
            <ul>
                {results.map((result, index) => (
                    <li key={index}>
                        <a href={result.url} onClick={() => onClick(result.url)}>
                            {result.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchResults;
