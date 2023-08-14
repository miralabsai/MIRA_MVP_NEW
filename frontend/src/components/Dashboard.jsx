import React from "react";
import "./Dashboard.css";
import logo from "../assets/cover.png";

function DashBoardPage() {
    return (
      <div className="chat-container">
        <div className="sidebar">
            <img src={logo} alt="MIRA Logo" className="mira-logo" />
            <nav className="sidebar-menu">
                <a href="#chat-interface" className="menu-item">Converse with Mira</a>
                <a href="#preapproval-interface" className="menu-item">Mira's Magic PreApproval</a>
                <a href="#document-manager-interface" className="menu-item">Mira's Document Wizard</a>
                <a href="#loan-application-interface" className="menu-item">Mira's LoanApp Lounge</a>
                <a href="#user-dashboard-interface" className="menu-item">Your Mira Dashboard</a>
            </nav>
            <div className="profile-signup-section">
                <button className="profile-button">
                <img src="path/to/avatar.png" alt="Profile" className="profile-icon" /> Profile
                </button>
                <button className="signup-button">Logout</button>
            </div>
        </div>
        <div className="main-content">
          <div className="profile-login">
            {/* Profile and login buttons */}
          </div>
          <div className="chat-interface">
            {/* Chat Interface */}
          </div>
        </div>
      </div>
    );
  }
  
  export default DashBoardPage;
