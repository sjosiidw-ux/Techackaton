import { useState, useEffect, useRef } from 'react';

export const useTraCIStream = (url) => {
  const [vehicles, setVehicles] = useState([]);
  const [systemMetrics, setMetrics] = useState({ 
    pressure: 0, 
    phase: 0, 
    fuelSaved: 0,
    history: Array(20).fill(0), // REQUIRED for LiveGraph
    logs: ["[SYSTEM] WAITING FOR SIGNAL..."] // REQUIRED for EventLog
  });

  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log("✅ Connected to SUMO TraCI Server");
      setMetrics(prev => ({ 
        ...prev, 
        logs: ["[SYSTEM] CONNECTION ESTABLISHED", ...prev.logs] 
      }));
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // 1. UPDATE VEHICLES
        // Expecting data.vehicles to be an array: [{ id, position: [x, y], ... }]
        if (data.vehicles) {
          setVehicles(data.vehicles);
        }

        // 2. UPDATE METRICS (Graph & Logs)
        setMetrics(prev => {
           // A. Update Graph History (Slide the window)
           const newPressure = data.pressure !== undefined ? data.pressure : prev.pressure;
           const newHistory = [...prev.history.slice(1), newPressure];
           
           // B. Update Logs (Only if backend sends a 'log_msg')
           let newLogs = prev.logs;
           if (data.log_msg) {
             const time = new Date().toLocaleTimeString('en-US', { hour12: false });
             newLogs = [`[${time}] ${data.log_msg}`, ...prev.logs].slice(0, 5);
           }

           return {
             pressure: newPressure,
             phase: data.phase !== undefined ? data.phase : prev.phase,
             fuelSaved: data.fuel_saved !== undefined ? data.fuel_saved : prev.fuelSaved,
             history: newHistory,
             logs: newLogs
           };
        });

      } catch (err) {
        console.error("❌ Parse Error:", err);
      }
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, [url]);

  return { vehicles, systemMetrics };
};