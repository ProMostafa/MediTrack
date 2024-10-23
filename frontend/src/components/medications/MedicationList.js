import React, { useEffect, useState } from 'react';
import { ToastContainer } from 'react-toastify';
import medicationService from '../../services/medicationService';
import refillService from '../../services/refillService';
import '../../style/medicationList.css';
import { useAuth } from '../../context/AuthContext';
import { successNotify, errorNotify } from '../common/notify';  


const MedicationList = () => {
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const { authData } = useAuth(); 
  const { token, userRole } = authData || {};

  useEffect(() => {
    const fetchMedications = async () => {
      if (!token) {
        return;
      }
      try {
        const data = await medicationService.getMedications(token);
        setMedications(data);
        setLoading(false);
      } catch (err) {
        errorNotify('Failed to load medications. Please try again later.');
        setLoading(false);
      }
    };
    fetchMedications();
  }, [token]);

  const handleRefillRequest = async (medicationId) => {
    try {
      await refillService.requestRefill(token, medicationId, 1);
      successNotify('Refill request submitted successfully!');
    } catch (err) {
      errorNotify('Failed to submit refill request. Please try again.');
    }
  };

  if (loading) {
    return <p>Loading medications...</p>;
  }

  return (
    <div className="medication-list-container">
      <h2>Available Medications</h2>
      <table className="medication-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Available Quantity</th>
            {userRole === 'patient' && <th>Action</th>}
          </tr>
        </thead>
        <tbody>
          {medications.map((med) => (
            <tr key={med.id}>
              <td>{med.name}</td>
              <td>{med.description}</td>
              <td>
                {med.available_quantity > 0 ? med.available_quantity : 'Not Available'}
              </td>
              {userRole === 'patient' && (
                <td>
                  {med.available_quantity > 0 ? (
                    <button
                      className="refill-button"
                      onClick={() => handleRefillRequest(med.id)}
                    >
                      Request Refill
                    </button>
                  ) : (
                    <button className="refill-button-disable" disabled>Request Refill</button>
                  )}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
      <ToastContainer />
    </div>
  );
};

export default MedicationList;
