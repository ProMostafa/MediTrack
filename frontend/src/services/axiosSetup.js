import axios from 'axios';
import authService from './authService';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_URL,
});

// Interceptors for handling token refresh
axiosInstance.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
      config.headers['Content-Type'] = `application/json`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {

      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh');
      if (refreshToken) {
        try {
          const { token, newRefresh } = await authService.refreshToken(refreshToken);
          localStorage.setItem('token', token);
          localStorage.setItem('refresh', newRefresh);
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          return axiosInstance(originalRequest);
        } catch (refreshError) {
          console.error('Refresh token failed:', refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
