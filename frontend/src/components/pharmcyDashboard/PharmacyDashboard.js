import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import DashboardStatisticsService from '../../services/dashboardService';
import { successNotify, errorNotify } from '../common/notify';  
import DonutChart from '../Charts/DonutChart';
import BarChart from '../Charts/BarChart';


const PharmacistDashboard = () => {
  const [prescriptionData, setPrescriptionData] = useState({
    requested_count: 0,
    pending_refills: 0,
    completed_refills: 0,
  });
  
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { authData } = useAuth(); 
  const { token } = authData || {};

  useEffect(() => {
    const fetchDashboardStatistics = async () => {
      if (!token) {
        return;
      }
      try {
        const data = await DashboardStatisticsService.getDashboardStatistics(token);
        setPrescriptionData(data);
      } catch (err) {
        setError('Failed to load refill requests. Please try again later.');
        errorNotify('Failed to load refill requests. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardStatistics();
  }, [token]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/refills/');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setPrescriptionData((prevData) => ({
          ...prevData,
          requested_count: data.message.requested_count || prevData.requested_count,
          pending_refills: data.message.pending_refills || prevData.pending_refills,
          completed_refills: data.message.completed_refills || prevData.completed_refills,
        }));
      }
    };

    ws.onerror = () => {
      setError('WebSocket connection error. Please check your connection.');
      errorNotify('WebSocket connection error. Please check your connection.');
    };

    return () => ws.close();
  }, []);


  if (loading) {
    return <div>Loading...</div>;
  }

  const { requested_count, pending_refills, completed_refills } = prescriptionData;
  const seriesData = [requested_count, pending_refills, completed_refills];
  const labels = ['Requested', 'Pending', 'Completed'];
  const chartTitle = 'Prescription Summary';
  const seriesDataV1 = [
    {
      name: 'Requested',
      data: [requested_count],
    },
    {
      name: 'Pending',
      data: [pending_refills],
    },
    {
      name: 'Completed',
      data: [completed_refills],
    },
  ];
  const categoriesV1 = ['Prescriptions'];

  return (
    <div>
      <h1>Pharmacist Dashboard</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <h2>Summary</h2>
        <p>Requested Prescriptions: {prescriptionData.requested_count}</p>
        <p>Pending Prescriptions: {prescriptionData.pending_refills}</p>
        <p>Filled Prescriptions: {prescriptionData.completed_refills}</p>
      </div>
      <DonutChart series={seriesData} title={chartTitle} labels={labels} />
      <BarChart series={seriesDataV1} title={chartTitle} categories={categoriesV1} />

    </div>
  );
};

export default PharmacistDashboard;
