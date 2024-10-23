import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import '../../style/navbar.css';
import logo from '../../assets/logo.png';

const Navbar = () => {
  const { authData, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <ul>

          {!authData.token ? (
            <>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </>
          ) : (
            <>
           
              {authData.userRole === 'patient' && (
                <>
                  <li><Link to="/medications">Medications</Link></li>
                  <li><Link to="/refill-requests">Refill Requests</Link></li>
                  <li><Link to="/patient-complete-refills">Completed Requests</Link></li>
                </>
              )}

              {authData.userRole === 'pharmacist' && (
                <>
                  <li><Link to="/dashboard">Dashboard</Link></li>
                  <li><Link to="/medications">Medications</Link></li>
                  <li><Link to="/pending-refill-requests">Pending Refills</Link></li>
                  <li><Link to="/pharmacist-complete-refills">Completed Refills</Link></li>
                </>
              )}

              <li><button onClick={logout}>Logout</button></li>
            </>
          )}
        </ul>
        <div className="navbar-logo">
          <img src={logo} alt="Logo" />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
