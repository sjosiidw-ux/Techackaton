import React from 'react';

export const EventLog = ({ logs = [] }) => {
  return (
    <div style={{
      marginTop: '15px',
      fontFamily: 'monospace',
      fontSize: '10px',
      color: '#00ff80',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      padding: '10px',
      borderRadius: '4px',
      border: '1px solid rgba(0, 255, 128, 0.2)',
      height: '80px',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column-reverse' // Newest logs at the bottom
    }}>
      {logs.map((log, i) => (
        <div key={i} style={{ opacity: 1 - (i * 0.2), marginBottom: '2px' }}>
          <span style={{ color: '#94a3b8' }}>&gt;</span> {log}
        </div>
      ))}
    </div>
  );
};