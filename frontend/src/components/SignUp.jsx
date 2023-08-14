// Desc: Sign Up page for the application
import React, { useState } from "react";
import { Link } from "react-router-dom";
 // Make sure to include this line if Bootstrap is not globally imported in your project
import "./UnlockMira.css";

function SignUp() {
  const [userType, setUserType] = useState('user');
  const [firstFocus] = React.useState(false);
  const [lastFocus] = React.useState(false);
  const [emailFocus] = React.useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [nmlsId, setNmlsId] = useState('');  // Only for Loan Officer
  const [setErrorMessage] = useState(''); // To store and display error messages

  const handleSignUp = async () => {
      if(password !== confirmPassword) {
          setErrorMessage('Passwords do not match.');
          return;
      }

      const userData = {
          username: email,  
          password: password,
          first_name: firstName,
          last_name: lastName,
          confirm_password: confirmPassword,
          role: userType === 'loanOfficer' ? 'Loan Officer' : 'Consumer'
      };
    

      if(userType === 'loanOfficer') {
          userData.nmlsId = nmlsId;  // Add NMLS ID for loan officers
      }

      const response = await fetch("http://localhost:8000/register/", {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData)
      });

      const data = await response.json();

      if(response.ok) {
          // Navigate the user to login page or any other suitable page
      } else {
          // Handle errors and display an error message
          setErrorMessage(data.detail || 'An error occurred during registration.');
      }
  }
  return (
    <div className="container">
      <div className="card card-signup">
        <div className="card-header">
          <nav className="nav-tabs-info justify-content-center">
            <button onClick={() => setUserType('user')} className={`nav-link ${userType === 'user' ? 'active' : ''}`}>User Login</button>
            <button onClick={() => setUserType('loanOfficer')} className={`nav-link ${userType === 'loanOfficer' ? 'active' : ''}`}>Loan Officer Login</button>
          </nav>
        </div>
        <div className="card-body">
        <form action="" className="form" method="">
            <h3 id="heading" className="title-up text-center">Sign Up</h3>
            <div className="field input-group">
              <input
                className="input-field"
                placeholder="First Name"
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </div>
            <div className="field input-group">
              <input
                className="input-field"
                placeholder="Last Name"
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
            </div>
            <div className="field input-group">
              <input
                className="input-field"
                placeholder="Email"
                type="text"
                value={email}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            {userType === 'loanOfficer' && (
              <div className="field input-group">
                <input
                  className="input-field"
                  placeholder="NMLS ID"
                  type="text"
                  value={nmlsId}
                  onChange={(e) => setNmlsId(e.target.value)}
                />
              </div>
            )}
            <div className="field input-group">
              <input
                className="input-field"
                placeholder="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="field input-group">
              <input
                className="input-field"
                placeholder="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
          </form>

        </div>
        <div className="card-footer">
          <button className="button1" onClick={handleSignUp}>Get Started</button>
          <button className="button2">Clear</button> <br />
        </div>  
      </div>
    </div>
  );
}

export default SignUp;