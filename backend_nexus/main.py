from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import app.simulation_core as sim_core
from app.intelligence import NexusBrain
NexusVision = None

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
# Choose real SUMO simulation if available, otherwise use the lightweight mock
if getattr(sim_core, 'traci', None) is None:
    print("⚠️ TraCI not available — using MockNexusSimulation for demo mode.")
    sim = sim_core.MockNexusSimulation(SUMO_CFG)
else:
    sim = sim_core.NexusSimulation(SUMO_CFG)
brain = NexusBrain()
vision = None

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

    # Try to initialize vision bridge lazily
    global NexusVision, vision
    try:
        from app.vision_bridge import NexusVision as _NexusVision
        NexusVision = _NexusVision
        vision = NexusVision()  # will fall back to logic-only if libs missing
    except Exception as e:
        vision = None
        print(f"⚠️ Vision bridge unavailable: {e}")

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
            real_pressure = vision.get_real_world_density() if vision else 0 # From Member 2
            
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