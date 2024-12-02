import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import Recommendations from './components/Recommendations';

const App = () => {
    const [searchResults, setSearchResults] = useState([]);
    const [recommendations, setRecommendations] = useState([]);

    const handleSearch = async (query) => {
        try {
            const response = await fetch(`http://localhost:5000/search?query=${query}`);
            const data = await response.json();
            setSearchResults(data.results);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    };

    const handleClick = async (url) => {
        try {
            const response = await fetch(`http://localhost:5000/recommend?clicked_url=${encodeURIComponent(url)}`);
            const data = await response.json();
            setRecommendations(data.recommendations);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    };

    return (
        <div>
            <SearchBar onSearch={handleSearch} />
            <SearchResults results={searchResults} onClick={handleClick} />
            <Recommendations items={recommendations} />
        </div>
    );
};

export default App;
