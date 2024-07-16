'use client'

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '../_components/navbar';
import style from '../style/Search.module.css';
import styleHome from '../style/Home.module.css';

export default function WatchMatch() {
    const [watchMatchRequest, setWatchMatchRequest] = useState(null);
    const [searchResults, setSearchResults] = useState<any[]>([]);
    const router = useRouter();

    useEffect(() => {
        const request = localStorage.getItem('watchMatchRequest');
        const searched = localStorage.getItem('searched');
        if (request) {
            setWatchMatchRequest(JSON.parse(request));
            localStorage.setItem('searched', "false");
            handleSearch(); 
        } else {
            localStorage.setItem('searched', "false");
            router.push('/');
        }
    }, []);

    const handleSearch = async () => {
        try {
            if (watchMatchRequest === null) {
                return;
            }
            const response = await fetch('http://localhost:5000/match/' + watchMatchRequest['watch_attributes'], {
                method: 'GET',
            });
            const data = await response.json();
            localStorage.setItem('searchResult', JSON.stringify(data));
            console.log('Search results:')
            console.log(data);
            setSearchResults(data);
        } catch (error) {
            console.error('Error:', error);
        }
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
                        </li>
                    ))}
                </ul>
            </div>
        );
    };

    return (
        <div>
            <Navbar />
            {watchMatchRequest ? (
                <div className={styleHome.search}>
                    <div className={style.watchContainer}>
                        <div className={style.watchContent}>
                            <div className={style.watchInformation}>
                                <p className={style.watchTitle}>{watchMatchRequest['brand']} {watchMatchRequest['family']}</p>                                
                                <div className={style.watchInformationText}>
                                    <p><span style={{fontWeight:"bold"}}>Watch Reference:</span> {watchMatchRequest['reference']}</p>
                                    <p><span style={{fontWeight:"bold"}}>Case Diameter:</span> {watchMatchRequest['caseDiameter']}</p>
                                    <p><span style={{fontWeight:"bold"}}>Watch Thickness:</span> {watchMatchRequest['caseHeight']}</p>
                                    <p><span style={{fontWeight:"bold"}}>Dial Color:</span> {watchMatchRequest['dialColor']}</p>
                                </div>
                            </div>
                            <img src={watchMatchRequest['image']} alt={`${watchMatchRequest['brand']} ${watchMatchRequest['family']} ${watchMatchRequest['reference']}`} className={style.watchImage}/>
                        </div>
                    </div>
                    {searchResults.length > 0 && <SearchResults searchResults={searchResults} />}
                </div>
            ) : (
                <p>No watch match request found.</p>
            )}
        </div>
    );
}