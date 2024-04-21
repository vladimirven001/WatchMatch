import React from 'react';
import Navbar from './_components/navbar';
import SearchBar from './_components/searchbar';
import style from './style/Home.module.css';

export default function Home() {
    return (
        <div>
            <Navbar />
            <div className={style.search}>
                <SearchBar />
            </div>
        </div>
    )
}