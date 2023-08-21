import React, { useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Chat_Mira from "./Chat_Mira";
import ProfilePage from "./ProfilePage";
import logo from "../assets/cover.png";
import "./Dashboard.css";

function DashBoardPage() {
  const [isProfileActive, setProfileActive] = useState(false);
  const navigate = useNavigate(); // Define the navigate function

  const handleProfileClick = () => {
    setProfileActive(!isProfileActive); // Toggle the profile active state
  };

  const handleLogout = () => {
    sessionStorage.removeItem('token'); // Clear the token from session storage
    localStorage.removeItem('token');   // Clear the token from local storage
    navigate('/'); // Navigate to the landing page or login page
  };
  
  return (
    <div className="chat-container">
      <div className="sidebar">
        <img src={logo} alt="MIRA Logo" className="mira-logo" />
        <nav className="sidebar-menu">
          <div onClick={() => navigate("chat-ui")} className="menu-item">
            Converse with Mira
          </div>
          <div onClick={() => navigate("miras-checkpoint")} className="menu-item">
            Mira's Checkpoint
          </div>
          <div onClick={() => navigate("miras-document-vault")} className="menu-item">
            Mira's Document Vault
          </div>
          <div onClick={() => navigate("miras-loanapp")} className="menu-item">
            Mira's LoanApp
          </div>
          <div onClick={() => navigate("your-miras-dashboard")} className="menu-item">
            Your Mira's Dashboard
          </div>
          {/* Other menu items */}
        </nav>
        <div className="profile-signup-section">
          <button className="profile-button" onClick={handleProfileClick}>
            Profile
          </button>
          <button className="signup-button" onClick={handleLogout}>Logout</button> {/* Added onClick handler */}
        </div>
      </div>
      <div className="main-content">
        <Routes>
          <Route path="chat-ui" element={<Chat_Mira />} />
          {/* Add other routes for other interfaces */}
        </Routes>
        {isProfileActive && <ProfilePage />}
      </div>
    </div>
  );
}

export default DashBoardPage;