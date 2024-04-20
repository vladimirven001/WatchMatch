'use client'

import React from 'react';
import style from '../style/style.module.css';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = ({ }) => {
    const router = useRouter();
    const pathname = usePathname();

    const navItems = [
        { text: 'WatchMatch', href: '/' },
        { text: 'About', href: '/about' },
        { text: 'Contact', href: '/contact' },
    ];

    return (
        <div className={style.navbarMainDiv}>
            {navItems.map((item, index) => (
                <div className={style.navbarContainer}>
                    <div key={index} className={`${style.navbarItem} ${pathname === item.href ? style.navbarItemActive : ''}`}>
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