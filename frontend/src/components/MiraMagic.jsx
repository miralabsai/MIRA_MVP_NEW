// MirasMagic.jsx

import React from 'react';
import './landingpage.css'; // Import the CSS file for this component

const MiraMagicSection = ({ isActive, onClose }) => {
    return (
      <div className={`mira-magic-section ${isActive ? 'active' : ''}`}>
        <button onClick={onClose} className="close-button">
          &times;
        </button>
        <h2 className="mira-magic-title">MIRA's Magic</h2><br />
        <div className="magic-content">
          <h3>For Users</h3>
          <ul>
            <li>AI-Powered Mortgage Chat: Engage with MIRA's intuitive chat interface, designed to understand and assist with your unique mortgage needs.</li>
            <li>Instant Qualification Insights: Receive immediate insights into your mortgage qualification status, backed by advanced algorithms.</li>
            <li>Custom-Tailored Mortgage Guidance: Benefit from personalized mortgage guidance that aligns with your financial goals and preferences.</li>
            <li>Real-Time Mortgage Updates: Stay up-to-date with real-time updates on your mortgage application status, every step of the way.</li>
          </ul><br />
          <h3>For Loan Officers</h3>
          <ul>
            <li>AI-Enhanced Client Outreach: Utilize AI-driven insights to reach out to clients with precision, maximizing engagement and success rates.</li>
            <li>Rapid Pre-Qualification Tools: Speed up the pre-qualification process with MIRA's intelligent tools, delivering instant results.</li>
            <li>Automated Document Processing: Automate document processing with MIRA's advanced AI, reducing manual workloads and errors.</li>
            <li>Intelligent Risk Assessment: Leverage MIRA's AI to assess risk with greater accuracy, and make more informed decisions.</li>
          </ul>
          <p>MIRA's Magic is in its ability to synthesize technology, efficiency, and human touch into a unified mortgage experience. Whether you're a borrower or a loan officer, MIRA's features are crafted to make your mortgage journey as smooth and rewarding as possible.</p>
        </div>
      </div>
    );
  };

export default MiraMagicSection;

  