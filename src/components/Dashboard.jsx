import React, { useState, useEffect } from 'react';
import MapView from './MapView';
import Sidebar from './Sidebar';
import StatsCard from './StatsCard';
import { TrendChart, ActivityChart, StateChart } from './Charts';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState('map');
  const [selectedYear, setSelectedYear] = useState('all');
  const [selectedState, setSelectedState] = useState('all');

  // Sample data for fallback
  const sampleData = {
    incidents: [
      {
        'Incident.year': 2020,
        'State': 'NSW',
        'Location': 'Byron Bay',
        'Latitude': -28.6474,
        'Longitude': 153.6020,
        'Victim.activity': 'Surfing'
      }
    ],
    yearly: {
      2018: 15,
      2019: 20,
      2020: 18,
      2021: 25,
      2022: 22
    },
    activities: {
      'Swimming': 30,
      'Surfing': 45,
      'Diving': 15,
      'Fishing': 10
    },
    states: {
      'NSW': 40,
      'QLD': 30,
      'WA': 20,
      'VIC': 10
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        console.log('Fetching data...');
        const response = await fetch('http://localhost:5349/data', {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Data received:', result);

        if (result.error) {
          throw new Error(result.error);
        }

        setData(result);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
        // Use sample data as fallback
        console.log('Using sample data due to fetch error');
        setData(sampleData);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    );
  }

  const getFilteredData = () => {
    if (!data?.incidents) return [];

    return data.incidents.filter(incident => {
      const yearMatch = selectedYear === 'all' ||
                       incident['Incident.year'].toString() === selectedYear;
      const stateMatch = selectedState === 'all' ||
                        incident.State === selectedState;
      return yearMatch && stateMatch;
    });
  };

  return (
    <div className="dashboard-container">
      <Sidebar
        view={view}
        setView={setView}
        selectedYear={selectedYear}
        setSelectedYear={setSelectedYear}
        selectedState={selectedState}
        setSelectedState={setSelectedState}
        data={data}
      />

      <main className="main-content">
        {error && (
          <div className="bg-red-500/10 border border-red-500 rounded-lg p-4 mb-4">
            <p className="text-red-500">Error loading data: {error}</p>
            <p className="text-gray-400 text-sm mt-1">Showing sample data instead</p>
          </div>
        )}

        <div className="stats-grid">
          <StatsCard
            title="Total Incidents"
            value={getFilteredData().length}
          />
          <StatsCard
            title="Most Active State"
            value={
              data?.states ?
                Object.entries(data.states).sort((a, b) => b[1] - a[1])[0][0]
                : '-'
            }
          />
          <StatsCard
            title="Common Activity"
            value={
              data?.activities ?
                Object.entries(data.activities).sort((a, b) => b[1] - a[1])[0][0]
                : '-'
            }
          />
        </div>

        <div className="chart-container">
          {view === 'map' && data && (
            <MapView
              data={getFilteredData()}
              selectedYear={selectedYear}
              selectedState={selectedState}
            />
          )}
          {view === 'trends' && data && (
            <TrendChart data={data.yearly} />
          )}
          {view === 'activities' && data && (
            <ActivityChart data={data.activities} />
          )}
          {view === 'states' && data && (
            <StateChart data={data.states} />
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;