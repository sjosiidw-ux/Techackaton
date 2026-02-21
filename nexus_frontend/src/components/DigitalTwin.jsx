import React from 'react';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';

// Pointing exactly at Hinjewadi Junction
const INITIAL_VIEW_STATE = {
  longitude: 73.74, 
  latitude: 18.59,  
  zoom: 17,
  pitch: 45,
  bearing: 0
};

export function DigitalTwin({ vehicles }) {
  // Creating a layer to render the vehicles
  const vehicleLayer = new ScatterplotLayer({
    id: 'vehicle-layer',
    data: vehicles || [],
    getPosition: d => d.position, 
    // DYNAMIC COLOR LOGIC:
    getFillColor: d => {
      // 1. If it's an ambulance, make it flash bright Red/White
      if (d.id && d.id.includes('ambulance')) return [255, 0, 50]; 
      
      // 2. If the car's speed is basically zero, it's stopped at a red light (Make it Orange/Red)
      if (d.speed < 0.5) return [255, 165, 0]; 
      
      // 3. Otherwise, it is driving normally on a green light (Make it Neon Green)
      return [0, 255, 128]; 
    },
    // Make the ambulance slightly bigger so the judges can see it!
    getRadius: d => (d.id && d.id.includes('ambulance') ? 6 : 3),                 
    radiusUnits: 'meters'
  });

  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: '#0f172a' }}>
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        layers={[vehicleLayer]}
      >
        {/* We are removing the broken map component and just rendering the dark background and the cars! */}
      </DeckGL>
    </div>
  );
}