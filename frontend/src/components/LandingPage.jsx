import React, { useState } from 'react';
import NavBar from './Navbar';
import FooterNav from './Footer';
import BackgroundVideo from './videoback';
import MeetMiraSection from './MeetMiraSection';
import MiraMagicSection from './MiraMagic';
import CareSection from './CareSection'; // Import CareSection
import UnlockMira from './UnlockMira';


const LandingPage = () => {
  const [activeSection, setActiveSection] = useState(null);

  // Function to close the active section
  const handleCloseSection = () => {
    setActiveSection(null);
  };

  return (
    <div className="relative h-screen z-0 overflow-hidden">
      <BackgroundVideo />
      <div className="absolute inset-0 flex flex-col h-full">
        <NavBar setActiveSection={setActiveSection} />
        <MeetMiraSection isActive={activeSection === 0} onClose={handleCloseSection} />
        <MiraMagicSection isActive={activeSection === 1} onClose={handleCloseSection} />
        <CareSection isActive={activeSection === 2} onClose={handleCloseSection} />
        <UnlockMira isActive={activeSection === 3} onClose={handleCloseSection} />
        <FooterNav />
      </div>  
    </div>
  );
};

export default LandingPage;
