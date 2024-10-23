import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

const AuthProvider = ({ children }) => {
  const [authData, setAuthData] = useState({
    token: null,
    refresh: null,
    userRole: null,
  });
  const [error, setError] = useState(null);
  const history = useNavigate();

  const login = async (username, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      console.log(response.ok)
      if (response.ok) {
        const { access: token, refresh, role: userRole } = data;
        
        setAuthData({ token, refresh, userRole });
        localStorage.setItem('token', token);
        localStorage.setItem('refresh', refresh);
        localStorage.setItem('role', userRole);

        history('/medications');
      } else {
        throw new Error(data.message || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Invalid username or password. Please try again.');
    }
  };

  const logout = () => {
    setAuthData({ token: null, refresh: null, userRole: null });
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    localStorage.removeItem('role');
    history('/login');
  };

  const refreshToken = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/accounts/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: authData.refresh }),
      });

      const data = await response.json();
      if (response.ok) {
        const { access: newToken } = data;
        setAuthData((prevState) => ({ ...prevState, token: newToken }));
        localStorage.setItem('token', newToken);
        return newToken;
      } else {
        throw new Error(data.message || 'Token refresh failed');
      }
    } catch (err) {
      console.error('Token refresh error:', err);
      logout();
    }
  };

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedRefresh = localStorage.getItem('refresh');
    const savedRole = localStorage.getItem('role');
    
    if (savedToken && savedRefresh && savedRole) {
      setAuthData({ token: savedToken, refresh: savedRefresh, userRole: savedRole });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ authData, setAuthData,login, logout ,error, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
