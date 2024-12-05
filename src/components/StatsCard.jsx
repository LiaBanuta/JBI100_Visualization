import React from 'react';

const StatsCard = ({ title, value, icon: Icon }) => {
  return (
    <div className="bg-gray-800 rounded-lg p-4 hover:bg-gray-700 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-400 text-sm font-medium">{title}</h3>
        {Icon && <Icon className="h-5 w-5 text-gray-400" />}
      </div>
      <div className="text-2xl font-bold text-white">{value}</div>
    </div>
  );
};

export default StatsCard;