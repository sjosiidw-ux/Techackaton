// import React from 'react';
// import { useMockData } from './hooks/useMockData';
// import { DigitalTwin } from './components/DigitalTwin';
// import { Failsafe } from './components/Failsafe';
// import { TrafficLight } from './components/TrafficLight';
// import { LiveGraph } from './components/LiveGraph';
// import { EventLog } from './components/EventLog'; // <-- Import added
// import { useTraCIStream } from './hooks/useTraCIStream'; // <-- Comment this out for now! (USE LATER FOR HACKATHON)

// function App() {
//   const { vehicles, systemMetrics } = useMockData(); 
//    const { vehicles, systemMetrics } = useTraCIStream("ws://localhost:8000/ws"); // <-- Comment this out for now! (USE LATER FOR HACKATHON)

//   return (
//     <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
//       <DigitalTwin vehicles={vehicles} />
//       <Failsafe /> 
      
//       {/* The Command Center HUD */}
//       <div style={{
//         position: 'absolute', top: 20, left: 20, padding: '20px',
//         backgroundColor: 'rgba(0, 0, 0, 0.7)', 
//         border: '1px solid rgba(255, 255, 255, 0.1)',
//         backdropFilter: 'blur(10px)',
//         borderRadius: '12px', zIndex: 10,
//         width: '250px' // Fixed width for cleaner look
//       }}>
//         <h2 style={{ margin: '0 0 15px 0', color: '#00ff80', letterSpacing: '2px' }}>
//           NEXUS COMMAND
//         </h2>
//         <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
//           <div>Active Vehicles: <strong>{vehicles.length}</strong></div>
//           <div>Road Pressure: <strong>{systemMetrics.pressure}</strong></div>
//           <div>Fuel Saved (₹): <strong style={{ color: '#4ade80' }}>{systemMetrics.fuelSaved}</strong></div>
          
//           <TrafficLight phase={systemMetrics.phase} />
//           <LiveGraph data={systemMetrics.history || Array(20).fill(0)} label="Congestion" />
          
//           {/* THE NEW TERMINAL LOG */}
//           <EventLog logs={systemMetrics.logs} />
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;
import React from 'react';
//import { useMockData} from './hooks/useMockData';  //<-- DISABLED MOCK
import { DigitalTwin } from './components/DigitalTwin';
import { Failsafe } from './components/Failsafe';
import { TrafficLight } from './components/TrafficLight';
import { LiveGraph } from './components/LiveGraph';
import { EventLog } from './components/EventLog'; 
import { useTraCIStream } from './hooks/useTraCIStream'; // <-- ENABLED LIVE

function App() {
  // const { vehicles, systemMetrics } = useMockData();  <-- DISABLED MOCK
  const { vehicles, systemMetrics } = useTraCIStream("ws://localhost:8000/ws"); // <-- ENABLED LIVE

  return (
    <div style={{ position: 'relative', width: '100vw', height: '100vh' }}>
      <DigitalTwin vehicles={vehicles} />
      <Failsafe /> 
      
      {/* The Command Center HUD */}
      <div style={{
        position: 'absolute', top: 20, left: 20, padding: '20px',
        backgroundColor: 'rgba(0, 0, 0, 0.7)', 
        border: '1px solid rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        borderRadius: '12px', zIndex: 10,
        width: '250px' 
      }}>
        <h2 style={{ margin: '0 0 15px 0', color: '#00ff80', letterSpacing: '2px' }}>
          NEXUS COMMAND
        </h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <div>Active Vehicles: <strong>{vehicles.length}</strong></div>
          <div>Road Pressure: <strong>{systemMetrics.pressure}</strong></div>
          <div>Fuel Saved (₹): <strong style={{ color: '#4ade80' }}>{systemMetrics.fuelSaved}</strong></div>
          
          <TrafficLight phase={systemMetrics.phase} />
          <LiveGraph data={systemMetrics.history || Array(20).fill(0)} label="Congestion" />
          
          <EventLog logs={systemMetrics.logs} />
        </div>
      </div>
    </div>
  );
}

export default App;