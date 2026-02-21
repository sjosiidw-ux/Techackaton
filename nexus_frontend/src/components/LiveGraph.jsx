import React from 'react';

export const LiveGraph = ({ data = [], color = '#00ff80', label }) => {
  // Simple math to scale the data points into an SVG path
  const width = 200;
  const height = 50;
  const maxVal = 40; // Assumed max pressure

  const points = data.map((val, i) => {
    const x = (i / (data.length - 1)) * width;
    const y = height - (val / maxVal) * height;
    return `${x},${y}`;
  }).join(' ');

  return (
    <div style={{ marginTop: '15px' }}>
      <div style={{ fontSize: '10px', color: '#94a3b8', marginBottom: '5px', textTransform: 'uppercase' }}>
        {label} HISTORY
      </div>
      <div style={{ 
        border: '1px solid rgba(255,255,255,0.1)', 
        background: 'rgba(0,0,0,0.3)', 
        padding: '5px',
        borderRadius: '4px'
      }}>
        <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
          {/* The glowing line */}
          <polyline
            fill="none"
            stroke={color}
            strokeWidth="2"
            points={points}
            vectorEffect="non-scaling-stroke"
            filter={`drop-shadow(0 0 4px ${color})`}
          />
        </svg>
      </div>
    </div>
  );
};