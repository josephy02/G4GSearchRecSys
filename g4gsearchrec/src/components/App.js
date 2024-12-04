import React, { useState } from 'react';
import SearchBar from './SearchBar';
import SearchResults from './SearchResults';
import Recommendations from './Recommendations';
import '../App.css'

const App = () => {
    const [searchResults, setSearchResults] = useState([]);
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async (query) => {
        setError(null);
        setIsLoading(true);
        try {
            const response = await fetch(
                `https://mdvmvbnt-5000.usw2.devtunnels.ms/search?query=${encodeURIComponent(query)}`,
                {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    },
                }
            );
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.results) {
                throw new Error('Invalid response format from server');
            }
            
            setSearchResults(data.results);
        } catch (error) {
            console.error('Error fetching search results:', error);
            setError(error.message || 'Failed to fetch search results. Please try again later.');
            setSearchResults([]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClick = async (url) => {
        try {
            const response = await fetch(
                `https://mdvmvbnt-5000.usw2.devtunnels.ms/recommend?clicked_url=${encodeURIComponent(url)}`,
                {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    },
                }
            );
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            setRecommendations(data.recommendations || []);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            setRecommendations([]);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="container mx-auto">
                <h1 className="text-3xl font-bold text-center mb-8">
                    Search & Recommendations
                </h1>
                
                <SearchBar onSearch={handleSearch} isLoading={isLoading} />
                
                {error && (
                    <div className="w-full max-w-2xl mx-auto mt-4 px-4">
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                            <span className="block sm:inline">{error}</span>
                        </div>
                    </div>
                )}
                
                <SearchResults 
                    results={searchResults} 
                    onClick={handleClick} 
                    isLoading={isLoading}
                />
                <Recommendations items={recommendations} />
            </div>
        </div>
    );
};

export default App;