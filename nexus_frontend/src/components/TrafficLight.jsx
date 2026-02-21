import React from 'react';

export const TrafficLight = ({ phase }) => {
  // Realistic intersection logic mapped to the 4 AI phases
  const isGreen = phase === 0;
  const isYellow = phase === 1;
  const isRed = phase === 2 || phase === 3 || phase === -1; // -1 included for our failsafe!

  // Glowing CSS effects for the active bulbs
  const getBulbStyle = (active, color, glowColor) => ({
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    backgroundColor: active ? color : '#1e293b', // Dim slate if off
    boxShadow: active ? `0 0 15px 5px ${glowColor}` : 'inset 0 0 5px rgba(0,0,0,0.5)',
    transition: 'all 0.3s ease-in-out'
  });

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      gap: '15px',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      padding: '10px 15px',
      borderRadius: '8px',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      marginTop: '15px'
    }}>
      <span style={{ fontSize: '12px', letterSpacing: '1px', color: '#94a3b8' }}>
        ACTIVE PHASE [{phase}]
      </span>
      
      {/* The Traffic Light Housing */}
      <div style={{
        display: 'flex',
        gap: '8px',
        backgroundColor: '#0f172a',
        padding: '6px',
        borderRadius: '20px',
        border: '1px solid #334155'
      }}>
        {/* Red Bulb */}
        <div style={getBulbStyle(isRed, '#ef4444', 'rgba(239, 68, 68, 0.6)')} />
        {/* Yellow Bulb */}
        <div style={getBulbStyle(isYellow, '#eab308', 'rgba(234, 179, 8, 0.6)')} />
        {/* Green Bulb */}
        <div style={getBulbStyle(isGreen, '#22c55e', 'rgba(34, 197, 94, 0.6)')} />
      </div>
    </div>
  );
};