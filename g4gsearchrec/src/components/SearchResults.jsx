import React from 'react';

const SearchResults = ({ results, onClick }) => {
    if (!results || results.length === 0) {
        return null;
    }

    return (
        <div className="w-full max-w-2xl mx-auto mt-8 px-4">
            <h2 className="text-xl font-semibold mb-4">Search Results</h2>
            <ul className="space-y-4">
                {results.map((result, index) => (
                    <li 
                        key={index}
                        className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                        <a 
                            href={result.url}
                            onClick={(e) => {
                                e.preventDefault();
                                onClick(result.url);
                            }}
                            className="text-blue-600 hover:text-blue-800 hover:underline"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            {result.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchResults;