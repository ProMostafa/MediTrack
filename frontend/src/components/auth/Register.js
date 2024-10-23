import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../../services/authService'; 
import '../../style/auth.css';  
import { successNotify, errorNotify } from '../common/notify';  

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('patient');  
  const [medicalHistory, setMedicalHistory] = useState('');
  const [pharmacyName, setPharmacyName] = useState('');
  const [licenseNumber, setLicenseNumber] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const history = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const registrationData = { username, password, role };
      
      if (role === 'patient') {
        registrationData.medical_history = medicalHistory;
        await authService.registerPatient(registrationData);
      } else if (role === 'pharmacist') {
        registrationData.pharmacy_name = pharmacyName;
        registrationData.license_number = licenseNumber;
        await authService.registerPharmacist(registrationData);
      }

      
      setSuccess(true);
      successNotify('Registration successful! Redirecting to login...');
      setTimeout(() => {
        history('/login');  
      }, 1500);
    } catch (err) {
      errorNotify('Registration failed. Please check your input and try again.');
    }
  };

  return (
    <div className="auth-container">
      <h2>Register</h2>
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">Registration successful! Redirecting to login...</p>}
      <form onSubmit={handleRegister}>
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Role:</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="patient">Patient</option>
            <option value="pharmacist">Pharmacist</option>
          </select>
        </div>
        
        {role === 'patient' && (
          <div className="form-group">
            <label>Medical History:</label>
            <textarea 
             style={{ width: '400px', height: '136px' }}
              value={medicalHistory}
              onChange={(e) => setMedicalHistory(e.target.value)}
              required
            />
          </div>
        )}
        
        {role === 'pharmacist' && (
          <>
            <div className="form-group">
              <label>Pharmacy Name:</label>
              <input
                type="text"
                value={pharmacyName}
                onChange={(e) => setPharmacyName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>License Number:</label>
              <input
                type="text"
                value={licenseNumber}
                onChange={(e) => setLicenseNumber(e.target.value)}
                required
              />
            </div>
          </>
        )}

        <button type="submit" className="auth-button">Register</button>
      </form>
    </div>
  );
};

export default Register;
