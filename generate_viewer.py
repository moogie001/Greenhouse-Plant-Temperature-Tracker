import os
import json

# Path to the Multitech RBS301 Temp Sensor folder
path_list = [
    "dataset/Multitech RBS301 Temp Sensor/7894e8000005874b",
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

# Generate HTML file with embedded data
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Temperature Sensor Data Viewer</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #151b3d;
            --bg-card: #1a2142;
            --accent-primary: #00d9ff;
            --accent-secondary: #7b2cbf;
            --text-primary: #e8eaf6;
            --text-secondary: #9fa8da;
            --border-color: #283167;
            --success: #00f5a0;
            --warning: #ffab00;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Space Grotesk', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(123, 44, 191, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 217, 255, 0.1) 0%, transparent 50%);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
            animation: fadeInDown 0.8s ease-out;
        }

        h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 300;
        }

        .search-section {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease-out 0.2s both;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .search-bar {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }

        input[type="text"], input[type="datetime-local"] {
            flex: 1;
            min-width: 200px;
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.1);
        }

        button {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            border: none;
            border-radius: 12px;
            padding: 1rem 2rem;
            color: white;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(0, 217, 255, 0.3);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(0, 217, 255, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: var(--bg-secondary) !important;
            box-shadow: none !important;
            border: 1px solid var(--border-color);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-primary);
            font-family: 'JetBrains Mono', monospace;
        }

        .data-table {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            overflow: hidden;
            animation: fadeInUp 0.8s ease-out 0.6s both;
        }

        .table-wrapper {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background: var(--bg-secondary);
        }

        th {
            padding: 1.2rem;
            text-align: left;
            font-weight: 600;
            color: var(--accent-primary);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.05em;
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
        }

        tbody tr {
            border-bottom: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }

        tbody tr:hover {
            background: rgba(0, 217, 255, 0.05);
        }

        td {
            padding: 1rem 1.2rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }

        .temp-value {
            color: var(--success);
            font-weight: 600;
            font-size: 1.1rem;
        }

        .battery-value {
            color: var(--warning);
        }

        .timestamp {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        .no-data {
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .filter-chips {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .chip {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .chip:hover {
            border-color: var(--accent-primary);
            background: rgba(0, 217, 255, 0.1);
        }

        .chip.active {
            background: var(--accent-primary);
            color: var(--bg-primary);
            border-color: var(--accent-primary);
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
            
            .search-bar {
                flex-direction: column;
            }
            
            input[type="text"], input[type="datetime-local"] {
                min-width: 100%;
            }
        }

        .chart-section {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease-out 0.5s both;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .chart-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--accent-primary);
            margin-bottom: 1.5rem;
            text-align: center;
        }

        .chart-container {
            position: relative;
            height: 400px;
            width: 100%;
        }

        @media (max-width: 768px) {
            .chart-container {
                height: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Sensor Data Viewer</h1>
            <p class="subtitle">Temperature Monitoring Dashboard</p>
        </header>

        <div class="search-section">
            <div class="search-bar">
                <input type="datetime-local" id="startTime" placeholder="Start Time">
                <input type="datetime-local" id="endTime" placeholder="End Time">
                <button onclick="filterData()">Search</button>
                <button class="btn-secondary" onclick="resetFilter()">Reset</button>
            </div>
            
            <div class="filter-chips">
                <div class="chip" onclick="quickFilter('today')">Today</div>
                <div class="chip" onclick="quickFilter('week')">Last 7 Days</div>
                <div class="chip" onclick="quickFilter('month')">Last 30 Days</div>
                <div class="chip" onclick="quickFilter('all')">All Time</div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Records</div>
                <div class="stat-value" id="totalRecords">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Temperature</div>
                <div class="stat-value" id="avgTemp">--</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Min Temperature</div>
                <div class="stat-value" id="minTemp">--</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Max Temperature</div>
                <div class="stat-value" id="maxTemp">--</div>
            </div>
        </div>

        <div class="chart-section">
            <h2 class="chart-title">📈 Temperature Over Time</h2>
            <div class="chart-container">
                <canvas id="temperatureChart"></canvas>
            </div>
        </div>

        <div class="data-table">
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Temperature (°C)</th>
                            <th>Battery (V)</th>
                            <th>RSSI</th>
                            <th>SNR</th>
                            <th>Port</th>
                        </tr>
                    </thead>
                    <tbody id="dataTableBody">
                        <tr>
                            <td colspan="6" class="no-data">Loading data...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Actual sensor data from Python
        let allData = DATA_PLACEHOLDER;
        let filteredData = [];
        let temperatureChart = null;

        function initChart() {
            const ctx = document.getElementById('temperatureChart').getContext('2d');
            
            temperatureChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Temperature (°C)',
                        data: [],
                        borderColor: '#00f5a0',
                        backgroundColor: 'rgba(0, 245, 160, 0.1)',
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 5,
                        pointBackgroundColor: '#00f5a0',
                        pointBorderColor: '#0a0e27',
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBackgroundColor: '#00d9ff',
                        pointHoverBorderColor: '#00f5a0',
                        pointHoverBorderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#e8eaf6',
                                font: {
                                    family: 'Space Grotesk',
                                    size: 14,
                                    weight: '600'
                                },
                                padding: 20
                            }
                        },
                        tooltip: {
                            backgroundColor: '#1a2142',
                            titleColor: '#00d9ff',
                            bodyColor: '#e8eaf6',
                            borderColor: '#283167',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: false,
                            titleFont: {
                                family: 'Space Grotesk',
                                size: 14,
                                weight: '600'
                            },
                            bodyFont: {
                                family: 'JetBrains Mono',
                                size: 13
                            },
                            callbacks: {
                                label: function(context) {
                                    return 'Temperature: ' + context.parsed.y.toFixed(1) + '°C';
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: '#283167',
                                drawBorder: false
                            },
                            ticks: {
                                color: '#9fa8da',
                                font: {
                                    family: 'JetBrains Mono',
                                    size: 11
                                },
                                maxRotation: 45,
                                minRotation: 45
                            }
                        },
                        y: {
                            grid: {
                                color: '#283167',
                                drawBorder: false
                            },
                            ticks: {
                                color: '#9fa8da',
                                font: {
                                    family: 'JetBrains Mono',
                                    size: 12
                                },
                                callback: function(value) {
                                    return value.toFixed(1) + '°C';
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        }

        function updateChart(data) {
            if (!temperatureChart) return;

            // Filter data to only include records with temperature
            const tempData = data.filter(d => d.object_data.temperature !== undefined && d.object_data.temperature !== null);
            
            // Prepare chart data
            const labels = tempData.map(d => formatDateShort(d.time));
            const temperatures = tempData.map(d => d.object_data.temperature);

            // Update chart
            temperatureChart.data.labels = labels;
            temperatureChart.data.datasets[0].data = temperatures;
            temperatureChart.update();
        }

        function formatDateShort(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }

        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        }

        function updateDisplay() {
            const tbody = document.getElementById('dataTableBody');
            
            if (filteredData.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="no-data">No data found for selected time range</td></tr>';
                updateStats([]);
                updateChart([]);
                return;
            }

            tbody.innerHTML = filteredData.map(record => `
                <tr>
                    <td class="timestamp">${formatDate(record.time)}</td>
                    <td class="temp-value">${record.object_data.temperature !== undefined ? record.object_data.temperature.toFixed(1) : '--'}</td>
                    <td class="battery-value">${record.battery !== null ? record.battery.toFixed(3) : '--'}</td>
                    <td>${record.rssi !== null ? record.rssi : '--'}</td>
                    <td>${record.snr !== null ? record.snr : '--'}</td>
                    <td>${record.fPort !== null ? record.fPort : '--'}</td>
                </tr>
            `).join('');

            updateStats(filteredData);
            updateChart(filteredData);
        }

        function updateStats(data) {
            document.getElementById('totalRecords').textContent = data.length;

            const temps = data.map(d => d.object_data.temperature).filter(t => t != null && t !== undefined);
            
            if (temps.length > 0) {
                const avg = temps.reduce((a, b) => a + b, 0) / temps.length;
                const min = Math.min(...temps);
                const max = Math.max(...temps);

                document.getElementById('avgTemp').textContent = avg.toFixed(1) + '°C';
                document.getElementById('minTemp').textContent = min.toFixed(1) + '°C';
                document.getElementById('maxTemp').textContent = max.toFixed(1) + '°C';
            } else {
                document.getElementById('avgTemp').textContent = '--';
                document.getElementById('minTemp').textContent = '--';
                document.getElementById('maxTemp').textContent = '--';
            }
        }

        function filterData() {
            const startTime = document.getElementById('startTime').value;
            const endTime = document.getElementById('endTime').value;

            if (!startTime && !endTime) {
                filteredData = [...allData];
            } else {
                filteredData = allData.filter(record => {
                    const recordTime = new Date(record.time);
                    const start = startTime ? new Date(startTime) : new Date(0);
                    const end = endTime ? new Date(endTime) : new Date();
                    return recordTime >= start && recordTime <= end;
                });
            }

            updateDisplay();
        }

        function resetFilter() {
            document.getElementById('startTime').value = '';
            document.getElementById('endTime').value = '';
            filteredData = [...allData];
            updateDisplay();
        }

        function quickFilter(period) {
            const now = new Date();
            let startDate;

            // Remove active class from all chips
            document.querySelectorAll('.chip').forEach(chip => chip.classList.remove('active'));
            
            // Add active class to clicked chip
            event.target.classList.add('active');

            switch(period) {
                case 'today':
                    startDate = new Date(now.setHours(0, 0, 0, 0));
                    break;
                case 'week':
                    startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                    break;
                case 'month':
                    startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
                    break;
                case 'all':
                    resetFilter();
                    return;
            }

            filteredData = allData.filter(record => {
                const recordTime = new Date(record.time);
                return recordTime >= startDate;
            });

            updateDisplay();
        }

        // Load data when page loads
        window.onload = function() {
            initChart();
            filteredData = [...allData];
            updateDisplay();
        };
    </script>
</body>
</html>'''

# Convert sensor data to JSON and embed in HTML
data_json = json.dumps(sensor_data_list, indent=2)
html_content = html_template.replace('DATA_PLACEHOLDER', data_json)

# Write HTML file
output_file = 'sensor_viewer.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\nHTML file generated successfully: {output_file}")
print(f"Open this file in your web browser to view the sensor data dashboard.")