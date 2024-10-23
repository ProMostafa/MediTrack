import axiosInstance from './axiosSetup';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';


const getDashboardStatistics = async (token) => {
    try {
        const response = await axiosInstance.get(`/api/medications/dashboard/`, {
        });
        return response.data;

    } catch (error) {
        console.error("Error completing refill request:", error);
        throw error;
    }

};


const DashboardStatisticsService = {
    getDashboardStatistics,
};

export default DashboardStatisticsService;
