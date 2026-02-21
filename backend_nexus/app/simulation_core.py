try:
    import traci
except Exception:
    traci = None

import sys
import os
from .utils import xy_to_latlon
import random
import math

class NexusSimulation:
    def __init__(self, config_path):
        self.config_path = config_path
        self.step_count = 0
        
    def start(self):
        """Initializes TraCI connection to SUMO"""
        if traci is None:
            raise RuntimeError("TraCI (SUMO) is not available on this system. Install SUMO and the Python traci package.")

        # Using 'sumo' for headless or 'sumo-gui' to see it open
        sumo_binary = "sumo"
        traci.start([sumo_binary, "-c", self.config_path])

    def step(self):
        """Advances simulation by one step"""
        if traci is None:
            raise RuntimeError("TraCI (SUMO) is not available; cannot step simulation.")
        traci.simulationStep()
        self.step_count += 1
    # Inside your vehicle extraction loop:

    def get_vehicle_payload(self):
        """
        Returns list of vehicles in the EXACT JSON format required by README.
        Format: { "id": "str", "position": [lon, lat] }
        """
        if traci is None:
            return []

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
        if traci is None:
            return 0

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
        if traci is None:
            print("⚠️ TraCI not available — cannot switch traffic light phase.")
            return
        traci.trafficlight.setPhase("J1", phase_index)

    def close(self):
        if traci is None:
            return
        traci.close()


class MockNexusSimulation:
    """A lightweight SUMO mock used when TraCI/SUMO isn't available.
    It simulates a handful of vehicles moving in a circle around the junction
    and exposes the same interface as `NexusSimulation` for the rest of the app.
    """
    def __init__(self, config_path=None):
        self.config_path = config_path
        self.step_count = 0
        self._running = False
        self._vehicles = []
        self._num_vehicles = 12
        self.current_phase = 0

        # Pre-generate vehicle ids and angles
        self._angles = [i * (2 * math.pi / self._num_vehicles) for i in range(self._num_vehicles)]

    def start(self):
        self._running = True
        self.step_count = 0
        # initialize vehicle dicts
        self._vehicles = [
            {"id": f"car_{i}", "x": 50 * math.cos(self._angles[i]), "y": 50 * math.sin(self._angles[i]), "speed": 5}
            for i in range(self._num_vehicles)
        ]

    def step(self):
        if not self._running:
            return
        # advance simulation: rotate vehicles slowly
        self.step_count += 1
        for i, v in enumerate(self._vehicles):
            # vehicles move along circular path; speed oscillates
            theta = self._angles[i] + 0.02 * self.step_count + 0.001 * i
            self._angles[i] = theta
            v['x'] = 50 * math.cos(theta)
            v['y'] = 50 * math.sin(theta)
            v['speed'] = max(0.1, 5 + math.sin(self.step_count / 10 + i) )

    def get_vehicle_payload(self):
        payload = []
        for v in self._vehicles:
            lon_lat = xy_to_latlon(v['x'], v['y'])
            payload.append({
                "id": v['id'],
                "position": lon_lat,
                "speed": v.get('speed', 0)
            })
        return payload

    def get_pressure(self):
        # Simple heuristic: more vehicles -> higher pressure; add small time-based variation
        base = len(self._vehicles) * 5
        variation = int((math.sin(self.step_count / 10) + 1) * 5)
        return min(base + variation, 100)

    def get_roi_metrics(self):
        return int(self.step_count * 0.5)

    def switch_phase(self, phase_index):
        self.current_phase = phase_index

    def close(self):
        self._running = False