import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const ActivityChart = ({ data }) => {
  const chartData = Object.entries(data).map(([activity, count]) => ({
    activity,
    count
  })).sort((a, b) => b.count - a.count);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="activity"
          stroke="#fff"
          angle={45}
          textAnchor="start"
          height={100}
        />
        <YAxis stroke="#fff" />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1f2937',
            border: '1px solid #374151',
          }}
        />
        <Bar dataKey="count" fill="#3b82f6" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default ActivityChart;