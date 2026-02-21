import os
import subprocess

def create_sumo_files():
    if not os.path.exists("sumo_config"):
        os.makedirs("sumo_config")

    # 1. Nodes (Intersection)
    with open("sumo_config/nexus.nod.xml", "w") as f:
        f.write("""<nodes>
    <node id="J1" x="0.0" y="0.0" type="traffic_light"/>
    <node id="n" x="0.0" y="300.0" type="priority"/>
    <node id="s" x="0.0" y="-300.0" type="priority"/>
    <node id="e" x="300.0" y="0.0" type="priority"/>
    <node id="w" x="-300.0" y="0.0" type="priority"/>
</nodes>""")

    # 2. Edges (Roads)
    with open("sumo_config/nexus.edg.xml", "w") as f:
        f.write("""<edges>
    <edge id="n_to_J1" from="n" to="J1" priority="1" numLanes="3" speed="15"/>
    <edge id="s_to_J1" from="s" to="J1" priority="1" numLanes="3" speed="15"/>
    <edge id="e_to_J1" from="e" to="J1" priority="1" numLanes="3" speed="15"/>
    <edge id="w_to_J1" from="w" to="J1" priority="1" numLanes="3" speed="15"/>
    <edge id="J1_to_n" from="J1" to="n" priority="1" numLanes="2" speed="15"/>
    <edge id="J1_to_s" from="J1" to="s" priority="1" numLanes="2" speed="15"/>
    <edge id="J1_to_e" from="J1" to="e" priority="1" numLanes="2" speed="15"/>
    <edge id="J1_to_w" from="J1" to="w" priority="1" numLanes="2" speed="15"/>
</edges>""")

    # 3. Generate Network
    try:
        subprocess.run(["netconvert", 
                        "--node-files=sumo_config/nexus.nod.xml", 
                        "--edge-files=sumo_config/nexus.edg.xml", 
                        "--output-file=sumo_config/nexus.net.xml"], check=True)
    except FileNotFoundError:
        print("❌ Error: SUMO tools not found. Please install Eclipse SUMO first.")
        return

    # 4. Traffic Flow (Routes)
    with open("sumo_config/nexus.rou.xml", "w") as f:
        f.write("""<routes>
    <vType id="car" accel="1.0" decel="4.5" length="5" maxSpeed="20" guiShape="passenger"/>
    <flow id="fn" begin="0" end="3600" probability="0.2" from="n_to_J1" to="J1_to_s" type="car"/>
    <flow id="fe" begin="0" end="3600" probability="0.15" from="e_to_J1" to="J1_to_w" type="car"/>
    <flow id="fs" begin="0" end="3600" probability="0.1" from="s_to_J1" to="J1_to_n" type="car"/>
    <flow id="fw" begin="0" end="3600" probability="0.1" from="w_to_J1" to="J1_to_e" type="car"/>
</routes>""")

    # 5. Configuration File
    with open("sumo_config/nexus.sumocfg", "w") as f:
        f.write("""<configuration>
    <input>
        <net-file value="nexus.net.xml"/>
        <route-files value="nexus.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="10000"/>
    </time>
</configuration>""")
    print("✅ SUMO Configuration Generated Successfully in /sumo_config")

if __name__ == "__main__":
    create_sumo_files()