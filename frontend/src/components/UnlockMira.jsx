import React from "react";
import SignUp from "./SignUp";
import Login from "./Login";
import "./UnlockMira.css";

const UnlockMira = ({ isActive, onClose }) => {
  return (
    <div className={`unlock-section ${isActive ? "active" : ""}`}>
      <button onClick={onClose} className="close-button">&times;</button>
      <h2 className="unlock-title">Unlock MIRA</h2>
      <div className="card-container">
        <div className="card-common">
          <SignUp />
        </div>
        <div className="card-common">
          <Login />
        </div>
      </div>
    </div>
  );
};

export default UnlockMira;
