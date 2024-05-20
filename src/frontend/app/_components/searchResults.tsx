'use client'

import React, { useEffect, useState } from 'react';

interface Watch {
    brand: string;
    caseBack: string;
    caseDiameter: string;
    caseGlass: string;
    caseHeight: string;
    caseLugWidth: string;
    caseMaterial: string;
    caseShape: string;
    dialColor: string;
    dialHands: string;
    dialIndexes: string;
    dialMaterial: string;
    family: string;
    image: string;
    limited: string;
    movement: string;
    name: string;
    price: string;
    produced: string;
    reference: string;
    watch_attributes: string;
}

const SearchResultsDisplay: React.FC = () => {
    const [watches, setWatches] = useState<Watch[]>([]);

    useEffect(() => {
        const updateWatches = () => {
            const storedData = localStorage.getItem('searchResult');
            if (storedData) {
                const data: Watch[] = JSON.parse(storedData);
                setWatches(data);
            }
        };

        // Initial load
        updateWatches();

        // Listen for changes
        const storageEventListener = (event: StorageEvent) => {
            if (event.key === 'searchResult') {
                updateWatches();
            }
        };

        window.addEventListener('storage', storageEventListener);

        // Cleanup
        return () => {
            window.removeEventListener('storage', storageEventListener);
        };
    }, []);

    return (
        <div>
            <h2>Watches</h2>
            <div>
                {watches.map((watch, index) => (
                    <div key={index} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px', width: '200px' }}>
                        <h3>{watch.brand}</h3>
                        <p>Price: ${watch.price}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchResultsDisplay;
