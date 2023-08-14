import React, { useState } from 'react';
import './landingpage.css';

const CareSection = ({ isActive, onClose }) => {
    const [activeIndex, setActiveIndex] = useState(null);
    const [userFaqsCollapsed, setUserFaqsCollapsed] = useState(false);
    const [officerFaqsCollapsed, setOfficerFaqsCollapsed] = useState(false); // New state variable for Loan Officers
  
    const toggleAccordion = (index) => {
      setActiveIndex(activeIndex === index ? null : index);
    };
  
    const toggleUserFaqs = () => {
      setUserFaqsCollapsed(!userFaqsCollapsed);
    };
  
    const toggleOfficerFaqs = () => { // New function to toggle Loan Officers FAQs
      setOfficerFaqsCollapsed(!officerFaqsCollapsed);
    };
  
    const content = `For Users
    What is MIRA and how can it assist me? MIRA isn't just another bot; it's your 24/7 AI-driven mortgage guide. Whether you have questions or need real-time application updates, MIRA's got you covered.
    How secure is my data with MIRA? Your peace of mind is our priority. MIRA employs top-notch encryption, ensuring your documents and details are protected against any unauthorized access.
    How does MIRA simplify the mortgage process for me? Think of MIRA as your mortgage compass. From faster eligibility checks, real-time application status updates, to seamless document submissions, MIRA streamlines each step, making your journey stress-free.
    Does MIRA replace human loan officers? Not at all! While MIRA handles routine inquiries and tasks, human experts remain invaluable for intricate issues or personalized advice.
    Is MIRA available 24/7. What if I have an urgent question overnight? Absolutely! MIRA operates round the clock. So whether it's a midnight query or an early morning eligibility check, MIRA's here to assist.
    For Loan Officers
    How does MIRA amplify my workflow? MIRA's your sidekick in automating repetitive tasks. From answering standard questions to pre-qualification, you can now dedicate more time to high-value interactions and closings.
    Can MIRA assist in lead generation? Yes, indeed! MIRA engages potential clients, sources leads, and qualifies them, ensuring you're connected with the most promising ones.
    Does MIRA oversee document collection and verification? MIRA goes beyond just gathering documents. Using advanced AI capabilities, it can review and extract critical information from these documents. Once the data is extracted, MIRA parses it into the system, updating relevant fields. This enables MIRA to review numbers and even pre-qualify clients. However, for nuanced or crucial verifications, we believe in the invaluable expertise of human loan officers. So, while MIRA handles the heavy lifting, final checks and balances remain in your capable hands.
    Will MIRA's AI approach make clients feel distant? Not a chance! MIRA offers a human-like chat experience, ensuring warmth in every interaction. And for deep-dives or tailored advice, they can always reach out to you.
    How seamlessly does MIRA integrate with my current systems, like Encompass or Calyx Software? MIRA's designed with compatibility in mind. Whether it's Encompass, Calyx Software, or other platforms, integration is smooth.
    Can MIRA help close deals faster. Does it boost productivity? Absolutely! With MIRA handling routine tasks, you can process loans quicker. That means more closings in less time and happy clients all around.`;
    
    const userSectionStart = content.indexOf('For Users');
    const officerSectionStart = content.indexOf('For Loan Officers');
    
    const userSection = content.substring(userSectionStart, officerSectionStart).replace('For Users', '').trim();
    const officerSection = content.substring(officerSectionStart).replace('For Loan Officers', '').trim();
    
    const userFaqs = userSection
      .split('\n')
      .map((line) => line.trim().split('? '));
    const officerFaqs = officerSection
      .split('\n')
      .map((line) => line.trim().split('? '));
  
    return (
    <div className={`care-section ${isActive ? 'active' : ''}`}>
        <button onClick={onClose} className="close-button">&times;</button>
        <h2 className="care-title">MIRA's Care</h2>
        <div className="care-content">
        <h3 onClick={toggleUserFaqs}>For Users {userFaqsCollapsed ? '▲' : '▼'}</h3>
        {!userFaqsCollapsed && userFaqs.map(([question, answer], index) => (
        <div key={index}>
            <button onClick={() => toggleAccordion(index)} className="accordion">
            {question}? {activeIndex === index ? '▲' : '▼'}
            </button>
            <div className={`panel ${activeIndex === index ? 'active' : ''}`}>
            {answer}
            </div>
        </div>
        ))}
        <h3 onClick={toggleOfficerFaqs}>For Loan Officers {officerFaqsCollapsed ? '▲' : '▼'}</h3>
        {!officerFaqsCollapsed && officerFaqs.map(([question, answer], index) => (
        <div key={index + userFaqs.length}>
            <button onClick={() => toggleAccordion(index + userFaqs.length)} className="accordion">
            {question}? {activeIndex === index + userFaqs.length ? '▲' : '▼'}
            </button>
            <div className={`panel ${activeIndex === index + userFaqs.length ? 'active' : ''}`}>
            {answer}
            </div>
        </div>
        ))}
    </div>
    </div>
    );
    };
    export default CareSection;