import React, { useState } from "react";
import SignUp from "./SignUp";
import Login from "./Login";
import "./UnlockMira.css";

const UnlockMira = ({ isActive, onClose }) => {
  const [isSignUp, setIsSignUp] = useState(true);

  return (
    <div className={`unlock-section ${isActive ? "active" : ""}`}>
      <button onClick={onClose} className="close-button">&times;</button>
      <h2 className="unlock-title">Unlock MIRA</h2>
      <div className={`flip-container ${isSignUp ? "" : "flip"}`}>
        <div className="flipper">
          <div className="front">
            <div className="card-common">
              <SignUp />
            </div>
          </div>
          <div className="back">
            <div className="card-common">
              <Login />
            </div>
          </div>
        </div>
      </div>
      <div className="toggle-auth-link">
        {isSignUp ? (
          <span onClick={() => setIsSignUp(false)}>Already have an Account? Login here!</span>
        ) : (
          <span onClick={() => setIsSignUp(true)}>Don't have an Account? Sign Up Here!</span>
        )}
      </div>
    </div>
  );
};

export default UnlockMira;