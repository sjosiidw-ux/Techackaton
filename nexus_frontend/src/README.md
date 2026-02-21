# NEXUS Frontend - Digital Twin Command Center

This is the React-based 3D Dashboard for Project NEXUS. It visualizes real-time traffic flow, road pressure, and AI decision-making.

## 🚀 Key Features
* **3D Digital Twin:** Isometric visualization of Hinjewadi Junction using Deck.gl.
* **Live Traffic Light:** Syncs visually with the AI's phase decisions.
* **Real-Time Graph:** Monitors congestion pressure history (60-second window).
* **System Event Log:** Displays the AI's internal decision logic in a scrolling terminal.
* **Emergency Failsafe:** Manual override capability for live demos.

## 🛠️ Setup Instructions
1.  **Install Dependencies:**
    ```bash
    npm install
    ```
2.  **Start the Dashboard:**
    ```bash
    npm run dev
    ```

## 🔌 Integration Guide (For Backend Team)
The app currently runs in **Demo Mode** using `useMockData`. To connect the live AI:

1.  Open `src/App.jsx`.
<!-- 2.  Look for the **"DATA SOURCE SWITCHER"** section (Lines 4-10). -->
3.  **Comment out** the Mock Data line:
    ```javascript
    // import { useMockData } from './hooks/useMockData';
    ```
4.  **Uncomment** the Live AI line:
    ```javascript
    import { useTraCIStream } from './hooks/useTraCIStream';
    ```
5.  Update the `App()` function to use the live hook:
    ```javascript
    // const { vehicles, systemMetrics } = useMockData(); // <--- Comment this
    const { vehicles, systemMetrics } = useTraCIStream("ws://localhost:8000/ws"); // <--- Uncomment this
    ```
## 📡 Backend API Requirements (JSON Schema)
The WebSocket must send data in this **exact** format for the Graph and Terminal to work:

```json
{
  "vehicles": [
     { "id": "car_1", "position": [73.74, 18.59] },
     { "id": "car_2", "position": [73.75, 18.60] }
  ],
  "pressure": 45,          // Integer (0-100) for the Live Graph
  "phase": 2,              // Integer (0-3) for the Traffic Light
  "fuel_saved": 150,       // Integer for the ROI Counter
  "log_msg": "Optimizing Green Window..."  // (Optional) String for the Terminal
}

##⚠️ IMPORTANT NOTE ON COORDINATES
The position array must be [Longitude, Latitude] (Geo-Coordinates).
Do not send x/y meters. If SUMO provides raw meters, convert them to Lat/Lon before sending via WebSocket, otherwise the cars will not appear on the map.

## 🚨 Demo Day Controls
* **Manual Override:** Press **`Ctrl + Shift + O`** to force a phase change signal to the backend API (/api/override).