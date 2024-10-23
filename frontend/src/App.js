import { Route, Routes } from 'react-router-dom';

import AuthProvider from './context/AuthContext';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import MedicationList from './components/medications/MedicationList';
import RefillRequestView from './components/patientRefills/RefillRequestView';
import CompleteRefillViewPatient from './components/patientRefills/CompleteRefillView';
import PendingRefillView from './components/pharmacistRefills/PendingRefillView';
import CompleteRefillViewPharmacist from './components/pharmacistRefills/CompleteRefillView';
import Navbar from './components/navbar/Navbar';
import PharmacyDashboard from './components/pharmcyDashboard/PharmacyDashboard'

function App() {
  return (
    <AuthProvider>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/medications" element={<MedicationList />} />
        <Route path="/refill-requests" element={<RefillRequestView />} />
        <Route path="/patient-complete-refills" element={<CompleteRefillViewPatient />} />
        <Route path="/pending-refill-requests" element={<PendingRefillView />} />
        <Route path="/pharmacist-complete-refills" element={<CompleteRefillViewPharmacist />} />
        <Route path="/dashboard" element={<PharmacyDashboard />} />

      </Routes>
    </AuthProvider>
  );
}

export default App;
