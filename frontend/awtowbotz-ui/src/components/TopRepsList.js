import React, { useEffect, useState } from 'react';
import axios from 'axios';
import BASE_URL from '../config';

function TopResults() {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchResults() {
      try {
        setIsLoading(true);
        setError(null);

        const response = await axios.get(`${BASE_URL}/api/current_data_live?station_id=top`);
        setResults(response.data?.results || []);
      } catch (err) {
        console.error('Error fetching top results:', err);
        setError('Failed to fetch top results.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchResults();
  }, []);

  return (
    <div className="top-results">
      <h3>Top Results</h3>

      {isLoading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!isLoading && results.length === 0 && <p>No data available.</p>}

      <ul>
        {results.map((item, index) => (
          <li key={index}>
            <strong>{item.label}:</strong> {item.value}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TopResults;