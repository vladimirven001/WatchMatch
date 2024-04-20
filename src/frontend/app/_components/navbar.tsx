'use client'

import React from 'react';
import style from '../style/Navbar.module.css';
import Link from 'next/link';
import { usePathname} from 'next/navigation';

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = ({ }) => {
    const pathname = usePathname();

    const navItems = [
        { text: 'WatchMatch', href: '/' },
    ];

    return (
        <div className={style.navbarMainDiv}>
            {navItems.map((item, index) => (
                <div key={index} className={style.navbarContainer}>
                    <div className={style.navbarItem}>
                        <Link href={item.href}>
                            {item.text}
                        </Link>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Navbar;