import axiosInstance from './axiosSetup';


const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const getMedications = async () => {
  const response = await axiosInstance.get(`/api/medications/`)
  return response.data;
};

const medicationService = {
  getMedications,
};

export default medicationService;
