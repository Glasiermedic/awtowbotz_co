import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

function RegionChart() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/api/sales_by_region')
      .then(res => {
        const labels = res.data.map(item => item.region);
        const data = res.data.map(item => item.total_sales);
        setChartData({
          labels,
          datasets: [{
            label: 'Sales by Region',
            data,
            backgroundColor: '#3b82f6',
            borderRadius: 6,
            barThickness: 40
          }]
        });
      })
      .catch(err => console.error('Error fetching region data:', err));
  }, []);

  if (!chartData) return <p>Loading chart...</p>;

  return (
    <div style={containerStyle}>
      <h3 style={headerStyle}>Sales by Region</h3>
      <Bar data={chartData} options={chartOptions} />
    </div>
  );
}

const containerStyle = {
  backgroundColor: '#fff',
  padding: '2rem',
  borderRadius: '0.5rem',
  boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
  marginBottom: '2rem',
  maxWidth: '800px',
  marginLeft: 'auto',
  marginRight: 'auto'
};

const headerStyle = {
  fontSize: '1.5rem',
  fontWeight: '700',
  marginBottom: '1rem',
  textAlign: 'center'
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: false },
    tooltip: {
      callbacks: {
        label: function (context) {
          return `$${context.raw.toLocaleString()}`;
        }
      }
    }
  },
  scales: {
    y: {
      ticks: {
        callback: function (value) {
          return `$${value.toLocaleString()}`;
        }
      }
    }
  }
};

export default RegionChart;
