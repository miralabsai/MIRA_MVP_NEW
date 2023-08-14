import React from 'react';
import './NavBar.css';

const NavBar = ({ setActiveSection }) => {
  const sections = [
    { title: 'Meet MIRA' },
    { title: "MIRA's Magic" },
    { title: "MIRA's Care" },
    { title: 'Unlock MIRA' }
  ];

  const handleSectionClick = (index, event) => {
    event.preventDefault();
    setActiveSection(index);
  };

  return (
    <div className="absolute top-0 left-0 w-full p-2 flex justify-between bg-transparent z-30">
      <div className="flex items-center title-glass">
        <img src="/profile.png" alt="Logo" className="h-20" />
      </div>
      <div className="flex items-center space-x-4 font-semibold">
        {sections.map((section, index) => (
          <button
            key={index}
            onClick={(event) => handleSectionClick(index, event)}
            className="text-dimWhite hover:text-white hover:rounded-2xl p-4 transition-all duration-300 title-glass"
          >
            {section.title}
          </button>
        ))}
      </div>
    </div>
  );
};

export default NavBar;
