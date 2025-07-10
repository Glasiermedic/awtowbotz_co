import React from 'react';
import SummaryCards from './components/SummaryCards'; //dependent on the config.js and .env working on fixing the issues
import RegionChart from './components/RegionChart';
import TopRepsList from './components/TopRepsList';

function App() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>aw-tow-botz-co: Transformer Co Sales Dashboard</h1>
      <SummaryCards />
      <RegionChart />
      <TopRepsList />
    </div>
  );
}

export default App;