import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Tooltip, Cell } from 'recharts';

const COLORS = ['#3b82f6', '#22c55e', '#ef4444', '#f59e0b', '#8b5cf6'];

const StateChart = ({ data }) => {
  const chartData = Object.entries(data).map(([state, count]) => ({
    state,
    count
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart>
        <Pie
          data={chartData}
          dataKey="count"
          nameKey="state"
          cx="50%"
          cy="50%"
          outerRadius={150}
          label
        >
          {chartData.map((entry, index) => (
            <Cell key={entry.state} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: '#1f2937',
            border: '1px solid #374151',
          }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default StateChart;