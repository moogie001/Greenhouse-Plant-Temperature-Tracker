import json
import base64
import struct
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------
# Configuration
# ----------------------------
DATASET_FILE = "flow_data.json"  # your JSON dataset file
# Thresholds for anomaly detection (adjust to your system)
MIN_FLOW_RATE = 1.0    # L/min, possible blockage
MAX_FLOW_RATE = 20.0   # L/min, possible overflow
LEAK_FLOW_RATE = 0.5   # L/min, possible leak

# ----------------------------
# Load dataset
# ----------------------------
with open(DATASET_FILE, "r") as f:
    dataset = json.load(f)

records = []

# ----------------------------
# Process each data point
# ----------------------------
for entry in dataset:
    # Parse timestamp
    ts = datetime.fromisoformat(entry["time"].replace("Z", "+00:00"))
    
    # Decode base64 sensor payload
    decoded = base64.b64decode(entry["data"])
    
    try:
        # Parse bytes (adjust struct format according to your sensor)
        # '>HHH' = Big-endian, 3 unsigned shorts (flow_rate, total_volume, battery)
        flow_rate, total_volume, battery_raw = struct.unpack('>HHH', decoded[:6])
        battery_voltage = battery_raw / 1000  # if stored in mV
    except struct.error:
        # Handle unexpected payload size
        print(f"Skipping record at {ts}: invalid payload size")
        continue

    # Detect anomaly
    if flow_rate < LEAK_FLOW_RATE:
        status = "Possible leak"
    elif flow_rate < MIN_FLOW_RATE:
        status = "Possible blockage"
    elif flow_rate > MAX_FLOW_RATE:
        status = "Overflow"
    else:
        status = "Normal"
    
    records.append({
        "timestamp": ts,
        "flow_rate": flow_rate,
        "total_volume": total_volume,
        "battery_voltage": battery_voltage,
        "status": status
    })

# ----------------------------
# Create DataFrame
# ----------------------------
df = pd.DataFrame(records)
print(df.head())

# ----------------------------
# Plot flow rate over time
# ----------------------------
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["flow_rate"], label="Flow rate (L/min)", color="blue")
plt.axhline(y=MIN_FLOW_RATE, color='orange', linestyle='--', label="Min Flow Threshold")
plt.axhline(y=MAX_FLOW_RATE, color='red', linestyle='--', label="Max Flow Threshold")
plt.axhline(y=LEAK_FLOW_RATE, color='purple', linestyle='--', label="Leak Threshold")
plt.scatter(df[df["status"]!="Normal"]["timestamp"], 
            df[df["status"]!="Normal"]["flow_rate"], 
            color='red', label='Anomaly', zorder=5)
plt.xlabel("Timestamp")
plt.ylabel("Flow rate (L/min)")
plt.title("Water Flow Rate Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()