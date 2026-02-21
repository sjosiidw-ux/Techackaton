from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.simulation_core import NexusSimulation
from app.intelligence import NexusBrain
from app.vision_bridge import NexusVision

app = FastAPI()

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Components
SUMO_CFG = "sumo_config/nexus.sumocfg"
sim = NexusSimulation(SUMO_CFG)
brain = NexusBrain()
vision = NexusVision() # Falls back to mock if no camera

simulation_running = False

@app.on_event("startup")
async def startup_event():
    global simulation_running
    try:
        sim.start()
        simulation_running = True
        print("✅ NEXUS Simulation Started")
    except Exception as e:
        print(f"❌ Failed to start SUMO: {e}\n(Did you run setup_sumo.py?)")

@app.on_event("shutdown")
def shutdown_event():
    sim.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 Frontend Connected")
    
    try:
        while simulation_running:
            # 1. Step the Physics
            sim.step()
            
            # 2. Collect Data
            sim_pressure = sim.get_pressure()
            real_pressure = vision.get_real_world_density() # From Member 2
            
            # 3. AI Decision
            new_phase, log = brain.decide(sim_pressure, real_pressure, 0)
            sim.switch_phase(new_phase)

            # 4. Construct JSON Payload (Strictly matching README)
            payload = {
                "vehicles": sim.get_vehicle_payload(),
                "pressure": max(sim_pressure, real_pressure),
                "phase": new_phase,
                "fuel_saved": sim.get_roi_metrics(),
                "log_msg": log
            }
            
            # 5. Send to Frontend
            await websocket.send_json(payload)
            await asyncio.sleep(0.05) # ~20 FPS
            
    except WebSocketDisconnect:
        print("Frontend Disconnected")

@app.post("/api/override")
async def manual_override():
    """Handles the Ctrl+Shift+O command from Frontend"""
    print("⚠️ MANUAL OVERRIDE TRIGGERED BY DEMO LEAD")
    return {"status": "Override Executed"}