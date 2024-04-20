import React, { useState } from 'react';

const SearchBar: React.FC = () => {
    const [searchText, setSearchText] = useState('');

    const handleSearch = async () => {
        try {
            // Call your Python backend API here
            const response = await fetch('/api/search', {
                method: 'POST',
                body: JSON.stringify({ searchText }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            // Handle the response from the backend
            const data = await response.json();
            console.log(data); // Do something with the response data
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
            />
            <button onClick={handleSearch}>
                <img src="/path/to/search-logo.png" alt="Search" />
            </button>
        </div>
    );
};

export default SearchBar;