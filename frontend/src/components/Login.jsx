import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import "./UnlockMira.css";

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/login/", {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              username: email,
              password: password
          })
      });
      const data = await response.json();

      if(response.ok) {
          setEmail('');
          setPassword('');
          sessionStorage.setItem('token', data.access_token);
          onLogin && onLogin();
          navigate('/Dashboard/chat-ui');
      } else {
          setErrorMessage(data.detail || 'An error occurred.');
      }
    } catch (error) {
      setErrorMessage('An unexpected error occurred. Please try again.');
    }
  };

  const handleClear = () => {
    setEmail('');
    setPassword('');
  };

  return (
    <div className="card card-login">
      <div className="card-header">
        <h3 className="title-up text-center">Login</h3>
      </div>
      <form action="" className="form" onSubmit={handleLogin}>
        <div className="card-body">
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          <div className="field input-group">
            <input
              className="input-field"
              placeholder="Email"
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="field input-group">
            <input
              className="input-field"
              placeholder="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>
        <div className="card-footer">
          <button className="button1" type="submit">Login</button>
          <button className="button2" type="button" onClick={handleClear}>Clear</button>
        </div>
      </form>
    </div>
  );
}

export default Login;