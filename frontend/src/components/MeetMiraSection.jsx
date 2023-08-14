// MeetMiraSection.jsx

import React from 'react';
import './landingpage.css'; // Import the CSS file for this component

const MeetMiraSection = ({ isActive, onClose }) => (
  <div className={`meet-mira-section ${isActive ? 'active' : ''}`}>
    <button onClick={onClose} className="close-button">
      &times; {/* HTML entity for "X" */}
    </button>
    <h2 className='meet-mira-title'>Meet MIRA</h2>
    <p>The Mortgage Intelligent Processing Assistant that is transforming the future of mortgage lending. MIRA transcends traditional barriers by combining innovative AI with human-centered design. This powerful partnership makes the mortgage process seamless for both lenders and borrowers.</p>
    <p>For lenders, MIRA is the key to unlocking efficiency. Its cutting-edge AI capabilities streamline every step of the mortgage lifecycle. Loan applications, risk assessments, approvals, and more are handled swiftly and accurately. MIRA's dynamic learning algorithms also continuously improve, ensuring lenders stay ahead. With MIRA, trusted partnerships are built on the foundations of speed and service.</p>
    <p>For borrowers, MIRA enables a transparent, personalized journey. Its AI generates tailored solutions that meet individual needs and goals. Interactions feel natural and intuitive, with the human touch still at the core. Borrowers understand exactly where they stand, and what steps come next. MIRA is always on hand to assist, answer questions, and guide borrowers down the optimal path.</p>
  </div>
);

export default MeetMiraSection;
