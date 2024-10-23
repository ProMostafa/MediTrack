// hooks/useFetch.js
import { useAuth } from '../context/AuthContext';

const useFetch = () => {
  const { authData, refreshToken } = useAuth();

  const fetchWithAuth = async (url, options = {}) => {
    let response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${authData.token}`,
      },
    });

    if (response.status === 401) {
      const newToken = await refreshToken();
      if (newToken) {
        response = await fetch(url, {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${newToken}`,
          },
        });
      }
    }

    return response;
  };

  return { fetchWithAuth };
};

export default useFetch;
