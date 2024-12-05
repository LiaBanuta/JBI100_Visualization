import React from 'react';

const Sidebar = ({
  view,
  setView,
  selectedYear,
  setSelectedYear,
  selectedState,
  setSelectedState
}) => {
  const yearOptions = ['all', '2018', '2019', '2020', '2021', '2022'];
  const stateOptions = ['all', 'NSW', 'QLD', 'WA', 'VIC', 'SA'];

  return (
    <aside className="sidebar">
      <h1 className="text-2xl font-bold mb-8">Shark Incidents</h1>

      {/* Navigation Buttons */}
      <div className="space-y-2 mb-8">
        <button
          onClick={() => setView('map')}
          className={`nav-button ${view === 'map' ? 'active' : ''}`}
        >
          Map View
        </button>
        <button
          onClick={() => setView('trends')}
          className={`nav-button ${view === 'trends' ? 'active' : ''}`}
        >
          Trends
        </button>
        <button
          onClick={() => setView('activities')}
          className={`nav-button ${view === 'activities' ? 'active' : ''}`}
        >
          Activities
        </button>
        <button
          onClick={() => setView('states')}
          className={`nav-button ${view === 'states' ? 'active' : ''}`}
        >
          State Distribution
        </button>
      </div>

      {/* Filters */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm text-gray-400 mb-2">
            Select Year
          </label>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="w-full bg-gray-700 text-white rounded p-2 border border-gray-600"
          >
            {yearOptions.map(year => (
              <option key={year} value={year}>
                {year === 'all' ? 'All Years' : year}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-2">
            Select State
          </label>
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="w-full bg-gray-700 text-white rounded p-2 border border-gray-600"
          >
            {stateOptions.map(state => (
              <option key={state} value={state}>
                {state === 'all' ? 'All States' : state}
              </option>
            ))}
          </select>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;