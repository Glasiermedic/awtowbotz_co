import React from 'react';
import SummaryCards from './components/SummaryCards';
import RegionChart from './components/RegionChart';
import TopRepsList from './components/TopRepsList';

function App() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>aw-tow-botz-co: Transformer Sales Dashboard</h1>
      <SummaryCards />
      <RegionChart />
      <TopRepsList />
    </div>
  );
}

export default App;