import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const TrendChart = ({ data }) => {
  // Convert data object to array format for Recharts
  const chartData = Object.entries(data).map(([year, count]) => ({
    year: parseInt(year),
    count
  })).sort((a, b) => a.year - b.year);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="year"
          stroke="#fff"
        />
        <YAxis
          stroke="#fff"
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1f2937',
            border: '1px solid #374151',
          }}
        />
        <Line
          type="monotone"
          dataKey="count"
          stroke="#22c55e"
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TrendChart;