import React, { useEffect, useState } from 'react';
import refillService from '../../services/refillService'; 
import { useAuth } from '../../context/AuthContext';
import '../../style/refillRequestView.css'; 

const RefillRequestView = () => {
  const [refillRequests, setRefillRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { authData } = useAuth(); 
  const { token } = authData || {};

  useEffect(() => {
    const fetchRefillRequests = async (refillStatus) => {
      if (!token) {
        return;
      }
      try {
        const data = await refillService.getRefillRequests(token, refillStatus = 'pending'); // Fetch refill requests with token
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
    <div className="refill-request-container">
      <h2>Pending Refill Requests</h2>
      {refillRequests.length === 0 ? (
        <p>No refill requests found.</p>
      ) : (
        <table className="refill-request-table">
          <thead>
            <tr>
              <th>Medication</th>
              <th>Quantity</th>
              <th>Date Submitted</th>
              <th>Status</th>
              <th>Fulfilled at</th>
            </tr>
          </thead>
          <tbody>
            {refillRequests.map((request) => (
              <tr key={request.id}>
                <td>{request.medication_name}</td>
                <td>{request.quantity}</td>
                <td>{new Date(request.requested_at).toLocaleDateString()}</td>
                <td>{request.status}</td>
                  <td>
                  {request.fulfilled_at ? new Date(request.fulfilled_at).toLocaleDateString() : '----------------'}
                  </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default RefillRequestView;
