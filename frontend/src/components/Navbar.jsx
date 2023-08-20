import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faTimes } from '@fortawesome/free-solid-svg-icons';
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

  const handleCloseMenu = () => {
    setMenuOpen(false);
  };

  // Function to close the menu when the Escape key is pressed
  const handleEscapeKeyPress = (event) => {
    if (event.key === 'Escape') {
      handleCloseMenu();
    }
  };

  useEffect(() => {
    // Add the event listener for the Escape key press
    window.addEventListener('keydown', handleEscapeKeyPress);
    return () => {
      // Remove the event listener when the component is unmounted
      window.removeEventListener('keydown', handleEscapeKeyPress);
    };
  }, []);

  return (
    <div className="absolute top-0 left-0 w-full p-2 flex justify-between bg-transparent z-30">
      <div className="flex items-center title-glass">
        <img src="/profile.png" alt="Logo" className="h-12 sm:h-20" />
      </div>
      <button className="sm:hidden text-xl" onClick={() => setMenuOpen(!menuOpen)}> {/* Mobile menu button */}
        <FontAwesomeIcon icon={faBars} style={{ color: 'white' }} />
      </button>
      {menuOpen && (
        <div className="mobile-menu-overlay">
          <div className="mobile-menu-container">
            <button className="close-button" onClick={handleCloseMenu}> {/* Close button */}
              <FontAwesomeIcon icon={faTimes} />
            </button>
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
