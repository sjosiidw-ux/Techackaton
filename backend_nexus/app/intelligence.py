class NexusBrain:
    def __init__(self):
        self.current_phase = 0
        self.time_in_phase = 0
    def decide_next_phase(self, vehicle_data):
        self.time_in_phase += 1
        
        # --- 🚨 EMERGENCY VEHICLE PREEMPTION (EVP) 🚨 ---
        for veh in vehicle_data:
            if "ambulance" in veh["id"].lower():
                log_msg = "🚨 AMBULANCE DETECTED! Forcing Green Light & Clearing Path!"
                # Logic to instantly switch to the ambulance's phase goes here
                # (You would set self.current_phase to whichever lane the ambulance is in)
                return self.current_phase, log_msg
                
        # ... (Rest of your normal pressure logic goes here) ...

    def decide(self, sim_pressure, real_pressure, active_phase):
        """
        Decides traffic light phase based on both Simulation and Real Vision data.
        """
        self.time_in_phase += 1
        
        # Fuse the data: Use the higher pressure reading (Sim vs Real)
        # Source 10: "Streaming continuous intelligence"
        combined_pressure = max(sim_pressure, real_pressure)
        
        log_msg = f"Pressure: {combined_pressure}% | Timer: {self.time_in_phase}"
        
        # Logic: Switch if pressure is high AND we've held green for > 5s (lowered from 10s)
        if combined_pressure > 40 and self.time_in_phase > 5:
            self.current_phase = (self.current_phase + 1) % 4
            self.time_in_phase = 0
            log_msg = f"⚠️ High Pressure ({combined_pressure})! Switching Phase."
        
        # Failsafe: Force switch if max timer reached (lowered from 45s to 15s)
        elif self.time_in_phase > 15:
            self.current_phase = (self.current_phase + 1) % 4
            self.time_in_phase = 0
            log_msg = "⏱️ Max Timer Reached. Cycling."

        return self.current_phase, log_msg