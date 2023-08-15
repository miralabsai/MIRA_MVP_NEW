import React from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import Chat_Mira from "./Chat_Mira";
import "./Dashboard.css";
import logo from "../assets/cover.png";

function DashBoardPage() {
  const navigate = useNavigate(); // Define the navigate function using useNavigate hook

  const handleLogout = () => {
    localStorage.removeItem('authToken'); // Clear the authentication token
    navigate('/'); // Redirect to the home page
  };

  return (
    <div className="chat-container">
      <div className="sidebar">
        <img src={logo} alt="MIRA Logo" className="mira-logo" />
        <nav className="sidebar-menu">
          <div onClick={() => navigate("chat-ui")} className="menu-item">
            Converse with Mira
          </div>
          {/* Other menu items */}
        </nav>
        <div className="profile-signup-section">
          <button className="profile-button">
            <img src="path/to/avatar.png" alt="Profile" className="profile-icon" /> Profile
          </button>
          <button className="signup-button" onClick={handleLogout}>Logout</button> {/* Add onClick handler */}
        </div>
      </div>
      <div className="main-content">
        <Routes>
          <Route path="chat-ui" element={<Chat_Mira />} /> {/* Change path to relative */}
          {/* Add other routes for other interfaces */}
        </Routes>
      </div>
    </div>
  );
}

export default DashBoardPage;
