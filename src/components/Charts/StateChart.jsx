import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';

const COLORS = ['#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#8b5cf6', '#06b6d4', '#ec4899'];

const StateChart = ({ data }) => {
  const chartData = Object.entries(data).map(([state, count]) => ({
    state,
    count
  }));

  const renderLabel = (entry) => {
    const RADIAN = Math.PI / 180;
    const radius = 140;
    const x = entry.cx + radius * Math.cos(-entry.midAngle * RADIAN);
    const y = entry.cy + radius * Math.sin(-entry.midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="#fff"
        textAnchor={x > entry.cx ? 'start' : 'end'}
        dominantBaseline="central"
        style={{ fontSize: '14px', fontWeight: '500', letterSpacing: '0.5px' }}
      >
        {entry.state}
      </text>
    );
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload?.[0]) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: '#1f2937',
          border: '1px solid #374151',
          padding: '12px 16px',
          borderRadius: '8px',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        }}>
          <p style={{
            margin: 0,
            color: '#fff',
            fontSize: '16px',
            fontWeight: 'bold'
          }}>
            {data.state}: {data.count}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={500}>
      <PieChart>
        <Pie
          data={chartData}
          dataKey="count"
          nameKey="state"
          cx="50%"
          cy="50%"
          outerRadius={120}
          innerRadius={0}
          fill="#8884d8"
          label={renderLabel}
          labelLine={false}
          paddingAngle={2}
        >
          {chartData.map((entry, index) => (
            <Cell
              key={entry.state}
              fill={COLORS[index % COLORS.length]}
              style={{ outline: 'none' }}
            />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default StateChart;