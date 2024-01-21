import React from 'react';
import stylesNavbar from '../styles/Navbar.module.css';
import Link from 'next/link';

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = ({ }) => {
    const navItems = [
        { text: 'WatchMatch', href: '/' },
        { text: 'About', href: './about' },
        { text: 'Contact', href: './contact' },
    ];

    return (
        <nav className="navbar">
            {navItems.map((item, index) => (
                <Link key={index} href={item.href} className={stylesNavbar.item}>
                    {item.text}
                </Link>
            ))}
        </nav>
    );
};

export default Navbar;