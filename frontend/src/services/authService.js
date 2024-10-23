import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/api/accounts/login/`, {
      username,
      password
    });
    const token = response.data.access; 
    const userRole = response.data.role; 
    const refresh = response.data.refresh;  

    return { token, refresh, userRole };
  } catch (err) {
    throw err
  }
};

const refreshToken = async (refresh) => {
  try {
    const response = await axios.post(`${API_URL}/api/accounts/refresh/`, { refresh });
    const token = response.data.access;
    const newRefresh = response.data.refresh;

    return { token, newRefresh };
  } catch (err) {
    throw err;
  }
};

const registerPatient = async (registrationData) => {
  try {
    await axios.post(`${API_URL}/api/accounts/register/`, {
      "username": registrationData.username,
      "password": registrationData.password,
      "role": registrationData.role,
      "patient_profile":{
        "medical_history": registrationData.medical_history || ""
      }
     
    });
  } catch (err) {
    throw err
  }

};

const registerPharmacist = async (registrationData) => {
  try {
    await axios.post(`${API_URL}/api/accounts/register/`, {
      username:registrationData.username,
      password:registrationData.password,
      role: registrationData.role,
      pharmacist_profile: {
        pharmacy_name: registrationData.pharmacy_name || "",
        license_number: registrationData.license_number || ""
      }
    });

  } catch (err) {
    throw err
  }
};

const authService = {
  registerPatient,
  registerPharmacist,
  login,
  refreshToken,
};

export default authService;
