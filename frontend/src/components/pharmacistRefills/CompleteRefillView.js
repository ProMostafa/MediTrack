import React, { useEffect, useState } from 'react';
import refillService from '../../services/refillService';
import { useAuth } from '../../context/AuthContext'; 
import '../../style/completeRefillView.css';

const CompleteRefillView = () => {
  const [refillRequests, setRefillRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { authData } = useAuth(); 
  const { token } = authData || {};

  useEffect(() => {
    const fetchRefillRequests = async (refillStatus) => {
      try {
        const data = await refillService.getRefillRequests(token, refillStatus = "completed"); // Fetch completed refill requests
        setRefillRequests(data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load refill requests. Please try again later.');
        setLoading(false);
      }
    };
    fetchRefillRequests();
  }, [token]);



  if (loading) {
    return <p>Loading refill requests...</p>;
  }

  if (error) {
    return <p className="error-message">{error}</p>;
  }

  return (
    <div className="complete-refill-container">
      <h2>Completed Refill Requests</h2>
      {refillRequests.length === 0 ? (
        <p>No complete refill requests found.</p>
      ) : (
        <table className="complete-refill-table">
          <thead>
            <tr>
              <th>Patient Name</th>
              <th>Medication</th>
              <th>Quantity</th>
              <th>Status</th>
              <th>Date Submitted</th>
              <th>Fulfilled by</th>
              <th>Fulfilled at</th>
            </tr>
          </thead>
          <tbody>
            {refillRequests.map((request) => (
              <tr key={request.id}>
                <td>{request.user_name}</td>
                <td>{request.medication_name}</td>
                <td>{request.quantity}</td>
                <td>{request.status}</td>
                <td>{new Date(request.requested_at).toLocaleDateString()}</td>
                <td>{request.fulfilled_by}</td>
                <td>{new Date(request.fulfilled_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default CompleteRefillView;
