import os
import json

# Path to the Multitech RBS301 Temp Sensor folder
# sensor_path = "dataset/Multitech RBS301 Temp Sensor/7894e80000054e0f"
# path_list = ["dataset/Multitech RBS301 Temp Sensor/7894e8000005874f"]
path_list = [
    "dataset/Multitech RBS301 Temp Sensor/7894e80000054e0a",
    "dataset/Multitech RBS301 Temp Sensor/7894e80000054e0b",
    "dataset/Multitech RBS301 Temp Sensor/7894e80000054e0c",
    "dataset/Multitech RBS301 Temp Sensor/7894e80000054e0e",
    "dataset/Multitech RBS301 Temp Sensor/7894e80000054e0f",
    "dataset/Multitech RBS301 Temp Sensor/7894e80000054e09",
    "dataset/Multitech RBS301 Temp Sensor/7894e8000005874b",
    "dataset/Multitech RBS301 Temp Sensor/7894e8000005874f"
]

# List to store all sensor data
sensor_data_list = []

# Read all JSON files in the folder
for folder in path_list:
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                
                # Extract relevant information
                record = {
                    'time': data.get('time'),
                    'fPort': data.get('fPort'),
                    'battery': data.get('object', {}).get('BAT'),
                    'object_data': data.get('object', {}),
                    'rssi': data.get('rxInfo', [{}])[0].get('rssi') if data.get('rxInfo') else None,
                    'snr': data.get('rxInfo', [{}])[0].get('snr') if data.get('rxInfo') else None
                }
                
                sensor_data_list.append(record)

# Sort by time
sensor_data_list.sort(key=lambda x: x['time'])

# Print summary
print(f"Loaded {len(sensor_data_list)} temperature sensor records")

if sensor_data_list:
    print(f"\nTime range: {sensor_data_list[0]['time']} to {sensor_data_list[-1]['time']}")
    
    # Show what different fPorts contain (filter out None values)
    print("\nUnique fPorts in dataset:")
    fports = set(record['fPort'] for record in sensor_data_list if record['fPort'] is not None)
    for port in sorted(fports):
        port_records = [r for r in sensor_data_list if r['fPort'] == port]
        print(f"  fPort {port}: {len(port_records)} records")
        if port_records:
            print(f"    Example data: {port_records[0]['object_data']}")
    
    # Check for records without fPort
    no_port = [r for r in sensor_data_list if r['fPort'] is None]
    if no_port:
        print(f"\n  Records without fPort: {len(no_port)}")
        print(f"    Example data: {no_port[0]['object_data']}")
    
    temp_count_list = {}
    count = 0
    for i in range(len(port_records)):
        if 'temperature' in port_records[i]['object_data']:
            count += 1
            if port_records[i]['object_data']['temperature'] not in temp_count_list:
                temp_count_list[port_records[i]['object_data']['temperature']] = 1
            else:
                temp_count_list[port_records[i]['object_data']['temperature']] += 1
            print(f"Temperature: {port_records[i]['object_data']['temperature']}")
    
    sorted_temp_count_list = sorted(temp_count_list.items())
    print(sorted_temp_count_list)
    print(f"\nTotal temperature readings: {count}")