import traci
import sys
import os
from .utils import xy_to_latlon

class NexusSimulation:
    def __init__(self, config_path):
        self.config_path = config_path
        self.step_count = 0
        
    def start(self):
        """Initializes TraCI connection to SUMO"""
        # Using 'sumo' for headless or 'sumo-gui' to see it open
        sumo_binary = "sumo" 
        traci.start([sumo_binary, "-c", self.config_path])

    def step(self):
        """Advances simulation by one step"""
        traci.simulationStep()
        self.step_count += 1
    # Inside your vehicle extraction loop:

    def get_vehicle_payload(self):
        """
        Returns list of vehicles in the EXACT JSON format required by README.
        Format: { "id": "str", "position": [lon, lat] }
        """
        vehicle_ids = traci.vehicle.getIDList()
        payload = []
        
        for vid in vehicle_ids:
            x, y = traci.vehicle.getPosition(vid)
            lon_lat = xy_to_latlon(x, y)
            payload.append({
                "id": vid,
                "position": lon_lat
            })
        return payload

    def get_pressure(self):
        """
        Calculates Queue Pressure (Source 35 in PDF).
        We sum the halting vehicles on all incoming lanes.
        """
        total_halted = 0
        # Iterate over all lanes to find stopped cars
        for lane in traci.lane.getIDList():
            total_halted += traci.lane.getLastStepHaltingNumber(lane)
        
        # Normalize to 0-100 for the frontend graph
        return min(total_halted * 5, 100) 

    def get_roi_metrics(self):
        """Calculates Fuel Saved (Source 219 in PDF)"""
        # Heuristic: Every step without gridlock saves virtual fuel
        return int(self.step_count * 0.45)

    def switch_phase(self, phase_index):
        """Actuates the physical traffic light (Source 134 in PDF)"""
        # 'J1' is the Junction ID defined in setup_sumo.py
        traci.trafficlight.setPhase("J1", phase_index)

    def close(self):
        traci.close()