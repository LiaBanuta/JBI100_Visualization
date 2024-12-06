import React from 'react';

const Sidebar = ({ view, setView, selectedYear, setSelectedYear, selectedState, setSelectedState, data }) => {
  const calculateStats = () => {
    if (!data?.incidents) return null;
    const total = data.incidents.length;
    const activities = data.incidents.reduce((acc, incident) => {
      const activity = incident['Victim.activity']?.toLowerCase() || '';
      if (activity.includes('swim')) acc.swimming++;
      if (activity.includes('surf')) acc.surfing++;
      if (activity.includes('div')) acc.diving++;
      if (activity.includes('fish')) acc.fishing++;
      return acc;
    }, { swimming: 0, surfing: 0, diving: 0, fishing: 0 });

    return Object.entries(activities).map(([key, value]) => ({
      activity: key,
      percentage: (value / total) * 100
    }));
  };

  const getFilteredYears = () => {
    if (!data?.yearly) return [];
    return Object.keys(data.yearly)
      .map(Number)
      .filter(year => year % 8 === 0)
      .sort((a, b) => b - a);
  };

  const stats = calculateStats() || [];
  const activityColors = {
    swimming: '#60a5fa',
    surfing: '#f87171',
    diving: '#4ade80',
    fishing: '#fbbf24'
  };

  return (
    <div className="sidebar">
      <h1 className="text-2xl font-bold text-white mb-8">Shark Incidents</h1>

      <nav className="mb-8">
        {['Map', 'Trends', 'Activities', 'State Distribution'].map(item => (
          <button
            key={item}
            onClick={() => setView(item.toLowerCase())}
            className={`nav-button ${view === item.toLowerCase() ? 'active' : ''}`}
          >
            {item}
          </button>
        ))}
      </nav>

      <div className="mb-8">
        <h2 className="text-xl text-white mb-4">Risk Levels</h2>
        {stats.map(({ activity, percentage }) => (
          <div key={activity} className="mb-1">
            <span
              className="text-sm"
              style={{ color: activityColors[activity] }}
            >
              {activity}:
            </span>
            <span className="text-sm ml-1" style={{ color: activityColors[activity] }}>
              {percentage.toFixed(1)}%
            </span>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <div>
          <div className="text-sm">Year</div>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="bg-white text-black px-3 py-1 w-32 rounded cursor-pointer outline-none"
          >
            <option value="all">All Years</option>
            {getFilteredYears().map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>

        <div>
          <div className="text-sm">State</div>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="bg-white text-black px-3 py-1 w-32 rounded cursor-pointer outline-none"
          >
            <option value="all">All States</option>
            {data?.states && Object.keys(data.states).sort().map(state => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;