'use client'

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import style from '../style/Search.module.css';
import { Button } from '@mui/base/Button';

const SearchBar: React.FC = () => {
    const [searchText, setSearchText] = useState('');
    const [isEmpty, setIsEmpty] = useState(false);
    const [searchResults, setSearchResults] = useState<any[]>([]);

    const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            if (searchText === '') {
                setIsEmpty(true);
                return; // Do not proceed if search text is empty
            } else {
                setIsEmpty(false);
            }
            const response = await fetch('http://localhost:5000/search/' + searchText, {
                method: 'GET',
            });
            const data = await response.json();
            localStorage.setItem('searchResult', JSON.stringify(data));
            console.log(data);
            setSearchResults(data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleKeyPress = async (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            await handleSearchResults();
        }
    };

    const handleSearchResults = () => {
        if (searchText !== '') {
            console.log('Search results:', searchResults);
        }
    };

    return (
        <div>
            <form className={style.form} onSubmit={handleSearch}>
                <div className={style.searchbarContainer}>
                    <span className="material-symbols-outlined" style={{fontSize:"30px", color:"#9CA3AF"}}>search</span>
                    <input
                        type="search"
                        value={searchText}
                        placeholder='Search watches'
                        onChange={(e) => {
                            setSearchText(e.target.value);
                            setIsEmpty(false);
                        }}
                        onKeyPress={handleKeyPress} // Call handleKeyPress on key press
                        className={style.searchbarInput}
                    />
                </div>
                {isEmpty && <p style={{ color: 'red', marginTop:'10px'}}>Please enter a search term</p>}
            </form>
            {searchText !== '' && <SearchResults searchResults={searchResults} />}
        </div>
    );
};

// Display search results
const SearchResults: React.FC<{ searchResults: any[] }> = ({ searchResults }) => {
    const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
    const router = useRouter();

    const toggleExpanded = (index: number) => {
        setExpandedIndex(index);
    };

    const handleWatchMatch = (watchAttributes: any) => {
        localStorage.setItem('watchMatchRequest', JSON.stringify(watchAttributes));
        localStorage.setItem('searched', "true");
        router.push('/watchmatch');
    };

    return (
        <div>
            <ul>
                {searchResults.map((result, index) => (
                    <li key={index} className={style.watchContainer} onClick={() => toggleExpanded(index)}>
                        <div className={style.watchContent}>
                            <div className={style.watchInformation}>
                                <p className={style.watchTitle}>{result.brand} {result.family}</p>                                
                                <div className={style.watchInformationText}>
                                    <p><span style={{fontWeight:"bold"}}>Watch Reference:</span> {result.reference}</p>
                                    <p><span style={{fontWeight:"bold"}}>Case Diameter:</span> {result.caseDiameter}</p>
                                    <p><span style={{fontWeight:"bold"}}>Watch Thickness:</span> {result.caseHeight}</p>
                                    <p><span style={{fontWeight:"bold"}}>Dial Color:</span> {result.dialColor}</p>
                                </div>
                            </div>
                            <img src={result.image} alt={`${result.brand} ${result.family} ${result.reference}`} className={style.watchImage}/>
                        </div>
                        {expandedIndex === index && (
                            <div className={style.watchMatchSearch}>
                                <div>
                                    <Button 
                                        className={style.watchSearchButton} 
                                        onClick={() => handleWatchMatch(result)}
                                    >
                                        Find watch matches
                                    </Button>
                                </div>
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchBar;