import React, { useEffect } from 'react';
import { BrowserRouter, Route, Routes, useNavigate, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import DashBoardPage from './components/Dashboard';

const PrivateRoute = ({ children }) => {
  const token = sessionStorage.getItem('token');

  return token ? children : <Navigate to="/" />;
};

const IdleTimeoutHandler = () => {
  const navigate = useNavigate();

  useEffect(() => {
    let idleTimer = null;
    const idleTimeout = 30 * 60 * 1000; // 30 minutes

    function resetIdleTimer() {
      if (idleTimer) clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        // Redirect to landing page
        navigate('/');
      }, idleTimeout);
    }

    window.addEventListener('mousemove', resetIdleTimer);
    window.addEventListener('mousedown', resetIdleTimer);
    window.addEventListener('keypress', resetIdleTimer);
    window.addEventListener('scroll', resetIdleTimer);

    resetIdleTimer(); // Start the timer

    return () => {
      // Cleanup listeners
      window.removeEventListener('mousemove', resetIdleTimer);
      window.removeEventListener('mousedown', resetIdleTimer);
      window.removeEventListener('keypress', resetIdleTimer);
      window.removeEventListener('scroll', resetIdleTimer);
    };
  }, [navigate]);

  return null; // This component does not render anything
};

const App = () => {
  return (
    <BrowserRouter>
      <IdleTimeoutHandler />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/Dashboard/*" element={
          <PrivateRoute>
            <DashBoardPage />
          </PrivateRoute>
        } />
        {/* Add other routes as needed */}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
