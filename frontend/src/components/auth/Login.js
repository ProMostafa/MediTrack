import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../../services/authService'; 
import { AuthContext } from '../../context/AuthContext';
import '../../style/auth.css';

const Login = () => {
  const { setAuthData } = useContext(AuthContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const history = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const { token, refresh,userRole } = await authService.login(username, password);
      setAuthData({ token, refresh,userRole });
      localStorage.setItem('token', token);
      localStorage.setItem('refresh', refresh); 
      localStorage.setItem('role', userRole);  
      history('/medications');
    } catch (err) {
      console.log(err)
      setError('Invalid username or password. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleLogin}>
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
        <button type="submit" className="auth-button">Login</button>
      </form>
    </div>
  );
};

export default Login;
