import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import './NavBar.css';

const NavBar = ({ setActiveSection }) => {
  const sections = [
    { title: 'Meet MIRA' },
    { title: "MIRA's Magic" },
    { title: "MIRA's Care" },
    { title: 'Unlock MIRA' },
  ];

  const [menuOpen, setMenuOpen] = useState(false);

  const handleSectionClick = (index, event) => {
    event.preventDefault();
    setActiveSection(index);
    setMenuOpen(false);
  };

  return (
    <div className="absolute top-0 left-0 w-full p-2 flex justify-between bg-transparent z-30">
      <div className="flex items-center title-glass">
        <img src="/profile.png" alt="Logo" className="h-12 sm:h-20" />
      </div>
      <div className="hidden sm:flex items-center space-x-4 font-semibold">
        {sections.map((section, index) => (
          <button
            key={index}
            onClick={(event) => handleSectionClick(index, event)}
            className="text-dimWhite hover:text-white hover:rounded-2xl p-2 sm:p-4 transition-all duration-300 title-glass"
          >
            {section.title}
          </button>
        ))}
      </div>
      <button className="sm:hidden text-xl" onClick={() => setMenuOpen(!menuOpen)}> {/* Mobile menu button */}
        <FontAwesomeIcon icon={faBars} style={{ color: 'white' }} />
      </button>
      {menuOpen && (
        <div className="mobile-menu-overlay">
          <div className="mobile-menu-container">
            {sections.map((section, index) => (
              <button
                key={index}
                onClick={(event) => handleSectionClick(index, event)}
                className="mobile-menu-item"
              >
                {section.title}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NavBar;
