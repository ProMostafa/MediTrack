import axiosInstance from './axiosSetup';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const requestRefill = async (token, medicationId, quantity) => {
  await axiosInstance.post(`/api/medications/refills/`, {
    medication: medicationId,
    quantity: quantity

  });
};


const getRefillRequests = async (token, status) => {
  const response = await axiosInstance.get(`/api/medications/refills/`, {
    params: {
      status: status,
    },
  });
  return response.data;
};

const completeRefillRequest = async (token, requestId) => {
  try {
    const response = await axiosInstance.post(
      `/api/medications/refills/complete/${requestId}/`,
      {},
    );
    return response.data;
  } catch (error) {
    console.error("Error completing refill request:", error);
    throw error;
  }
};

const refillService = {
  requestRefill,
  getRefillRequests, 
  completeRefillRequest,
};

export default refillService;
