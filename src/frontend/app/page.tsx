'use client'

import React, { useEffect } from 'react';
import Navbar from './_components/navbar';
import SearchBar from './_components/search';
import style from './style/Home.module.css';

export default function Home() {

    useEffect(() => {
        localStorage.removeItem('watchMatchRequest');
    }, []);

    return (
        <div>
            <Navbar />
            <div className={style.search}>
                <SearchBar />
            </div>
        </div>
    )
}