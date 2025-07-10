import React, { useEffect, useState } from 'react';
import axios from 'axios';

function TopRepsList() {
  const [reps, setReps] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/top_reps')
      .then(res => setReps(res.data))
      .catch(err => console.error('Error fetching top reps:', err));
  }, []);

  return (
    <div style={containerStyle}>
      <h3 style={headerStyle}>Top Sales Reps</h3>
      <ul style={{ paddingLeft: 0, listStyleType: 'none', width: '100%' }}>
        {reps.map((rep, index) => (
          <li key={index} style={itemStyle}>
            <span style={{ fontWeight: '600', fontSize: '1rem' }}>{rep.sales_rep}</span>
            <span style={{ float: 'right', fontSize: '1rem', color: '#2563eb' }}>${rep.total_sales.toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

const containerStyle = {
  backgroundColor: '#fff',
  padding: '1.5rem',
  borderRadius: '0.5rem',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.05)',
  marginBottom: '2rem',
  maxWidth: '600px',
  marginLeft: 'auto',
  marginRight: 'auto'
};

const headerStyle = {
  fontSize: '1.5rem',
  borderBottom: '2px solid #e2e8f0',
  paddingBottom: '0.5rem',
  marginBottom: '1rem',
  textAlign: 'center',
  fontWeight: '700'
};

const itemStyle = {
  marginBottom: '0.75rem',
  padding: '0.75rem 1rem',
  backgroundColor: '#f9fafb',
  borderRadius: '0.4rem',
  border: '1px solid #e5e7eb',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  transition: 'background 0.2s ease-in-out',
};

export default TopRepsList;
