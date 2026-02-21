import { useState, useEffect, useRef } from 'react';

const BASE_LON = 73.74;
const BASE_LAT = 18.59;

const LOG_MESSAGES = [
  "OPTIMIZING TRAFFIC FLOW...",
  "DETECTING VEHICLE DENSITY...",
  "UPDATING SIGNAL PHASE...",
  "CALCULATING FUEL SAVINGS...",
  "SYNCING WITH SENSORS...",
  "ADJUSTING GREEN WINDOW..."
];

const generateInitialVehicles = () => {
  return Array.from({ length: 50 }).map((_, i) => {
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.000015 + Math.random() * 0.00001;
    return {
      id: `veh_${i}`,
      position: [
        BASE_LON + (Math.random() - 0.5) * 0.005, 
        BASE_LAT + (Math.random() - 0.5) * 0.005
      ],
      velocity: [Math.cos(angle) * speed, Math.sin(angle) * speed]
    };
  });
};

export const useMockData = () => {
  const [vehicles, setVehicles] = useState(generateInitialVehicles);
  const [systemMetrics, setMetrics] = useState({ 
    pressure: 12, 
    phase: 0, 
    fuelSaved: 450,
    history: Array(20).fill(10),
    logs: ["[SYSTEM] NEXUS ONLINE"] // Start with one log
  });
  
  const requestRef = useRef();

  useEffect(() => {
    // 1. Animation Loop
    const animate = () => {
      setVehicles(prev => prev.map(v => ({
        ...v,
        position: [
          v.position[0] + v.velocity[0],
          v.position[1] + v.velocity[1]
        ]
      })));
      requestRef.current = requestAnimationFrame(animate);
    };
    requestRef.current = requestAnimationFrame(animate);

    // 2. Metrics & Logs Loop
    const metricInterval = setInterval(() => {
      setMetrics(prev => {
        const newPressure = Math.floor(Math.random() * 30);
        const newHistory = [...prev.history.slice(1), newPressure];
        
        // Randomly add a log message
        let newLogs = prev.logs;
        if (Math.random() > 0.3) { // 70% chance to add a log
           const randomMsg = LOG_MESSAGES[Math.floor(Math.random() * LOG_MESSAGES.length)];
           const time = new Date().toLocaleTimeString('en-US', { hour12: false, hour: "numeric", minute: "numeric", second: "numeric"});
           newLogs = [`[${time}] ${randomMsg}`, ...prev.logs].slice(0, 5); // Keep only last 5
        }

        return {
          pressure: newPressure,
          phase: (prev.phase + 1) % 4,
          fuelSaved: prev.fuelSaved + Math.floor(Math.random() * 10),
          history: newHistory,
          logs: newLogs
        };
      });
    }, 1000);

    return () => {
      cancelAnimationFrame(requestRef.current);
      clearInterval(metricInterval);
    };
  }, []);

  return { vehicles, systemMetrics };
};