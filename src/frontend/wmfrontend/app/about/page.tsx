import React from 'react';
import Navbar from '../_components/navbar';
import styles from '../styles/WatchMatch.module.css';

const App: React.FC = () => {
    return (
        <div className={styles.mainDiv}>
            <Navbar />
        </div>
    );
};

export default App;