'use client'

import React, { useState } from 'react';
import style from '../style/Searchbar.module.css';

const SearchBar: React.FC = () => {
    const [searchText, setSearchText] = useState('');

    const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/search/' + searchText, {
                method: 'GET',
            });
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    //     if (e.key === 'Enter') {
    //         handleSearch();
    //     }
    // };

    return (
        <form onSubmit={handleSearch}>
            <div className={style.searchbarContainer}>
                <span className="material-symbols-outlined" style={{fontSize:"30px", color:"#9CA3AF"}}>search</span>
                <input
                    type="search"
                    value={searchText}
                    placeholder='Search watches'
                    onChange={(e) => setSearchText(e.target.value)}
                    // onKeyDown={handleKeyDown}
                    className={style.searchbarInput}
                />
            </div>
        </form>
    );
};

export default SearchBar;