import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import LandingPage from './components/LandingPage' // Import the LandingPage component
import DashBoardPage from './components/Dashboard';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/Dashboard" element={<DashBoardPage />} />
        {/* Add other routes as needed */}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
