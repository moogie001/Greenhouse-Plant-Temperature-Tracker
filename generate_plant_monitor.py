import os
import json

# Path to the Multitech RBS301 Temp Sensor folder
path_list = [
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

# Generate HTML file with embedded data
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Temperature Risk Monitor</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --cream: #faf8f3;
            --dark-green: #1a3a1f;
            --forest-green: #2d5f3d;
            --sage: #8b9d83;
            --terracotta: #c86b4a;
            --warning-orange: #e6934e;
            --danger-red: #d64545;
            --text-dark: #2c2c2c;
            --text-light: #6b6b6b;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--cream);
            color: var(--text-dark);
            line-height: 1.6;
            background-image: 
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(138, 157, 131, 0.03) 2px, rgba(138, 157, 131, 0.03) 4px);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }

        header {
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid var(--sage);
        }

        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 900;
            color: var(--dark-green);
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            font-size: 1.1rem;
            color: var(--text-light);
            font-weight: 300;
        }

        .search-section {
            background: white;
            border-radius: 24px;
            padding: 2.5rem;
            margin-bottom: 3rem;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
        }

        .search-label {
            font-size: 1rem;
            font-weight: 600;
            color: var(--dark-green);
            margin-bottom: 1rem;
            display: block;
        }

        .search-bar {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        input[type="datetime-local"] {
            flex: 1;
            background: var(--cream);
            border: 2px solid var(--sage);
            border-radius: 16px;
            padding: 1.2rem 1.5rem;
            color: var(--text-dark);
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus {
            outline: none;
            border-color: var(--forest-green);
            background: white;
        }

        button {
            background: var(--forest-green);
            border: none;
            border-radius: 16px;
            padding: 1.2rem 2.5rem;
            color: white;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            background: var(--dark-green);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(26, 58, 31, 0.2);
        }

        .temperature-display {
            background: linear-gradient(135deg, var(--forest-green), var(--dark-green));
            border-radius: 24px;
            padding: 3rem;
            margin-bottom: 3rem;
            text-align: center;
            color: white;
            box-shadow: 0 12px 48px rgba(26, 58, 31, 0.3);
        }

        .temp-label {
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            opacity: 0.9;
            margin-bottom: 1rem;
        }

        .temp-value {
            font-family: 'Playfair Display', serif;
            font-size: 6rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .temp-timestamp {
            font-size: 0.95rem;
            opacity: 0.8;
        }

        .plants-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .plant-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
            position: relative;
        }

        .plant-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
        }

        .plant-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            background: linear-gradient(135deg, var(--sage), var(--forest-green));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
        }

        .danger-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            padding: 0.5rem 1rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: white;
        }

        .danger-low { background: var(--forest-green); }
        .danger-moderate { background: var(--warning-orange); }
        .danger-high { background: var(--terracotta); }
        .danger-critical { background: var(--danger-red); animation: pulse 2s infinite; }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }

        .plant-content {
            padding: 1.5rem;
        }

        .plant-name {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--dark-green);
            margin-bottom: 0.5rem;
        }

        .plant-scientific {
            font-style: italic;
            color: var(--text-light);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .plant-details {
            color: var(--text-dark);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        .temp-range {
            background: var(--cream);
            padding: 1rem;
            border-radius: 12px;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }

        .temp-range-label {
            font-weight: 600;
            color: var(--dark-green);
            margin-bottom: 0.3rem;
        }

        .add-plant-btn {
            background: var(--cream);
            border: 2px dashed var(--sage);
            border-radius: 20px;
            padding: 3rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            min-height: 400px;
        }

        .add-plant-btn:hover {
            border-color: var(--forest-green);
            background: white;
        }

        .add-icon {
            font-size: 4rem;
            color: var(--sage);
            margin-bottom: 1rem;
        }

        .add-text {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-light);
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            border-radius: 24px;
            padding: 2.5rem;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
        }

        .modal-title {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--dark-green);
            margin-bottom: 2rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            font-weight: 600;
            color: var(--dark-green);
            margin-bottom: 0.5rem;
        }

        input[type="text"],
        input[type="number"],
        input[type="url"],
        textarea {
            width: 100%;
            background: var(--cream);
            border: 2px solid var(--sage);
            border-radius: 12px;
            padding: 0.8rem 1rem;
            color: var(--text-dark);
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        textarea {
            resize: vertical;
            min-height: 100px;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: var(--forest-green);
        }

        .button-group {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }

        .btn-cancel {
            background: var(--sage);
        }

        .btn-cancel:hover {
            background: var(--text-light);
        }

        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-light);
        }

        .empty-icon {
            font-size: 5rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        .delete-btn {
            background: var(--danger-red);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            margin-top: 1rem;
            width: 100%;
        }

        .delete-btn:hover {
            background: #b33939;
        }

        .calendar-container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
        }

        .calendar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }

        .calendar-month {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--dark-green);
        }

        .calendar-nav {
            display: flex;
            gap: 1rem;
        }

        .nav-btn {
            background: var(--cream);
            border: 2px solid var(--sage);
            border-radius: 12px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 1.2rem;
            transition: all 0.3s ease;
        }

        .nav-btn:hover {
            background: var(--forest-green);
            color: white;
            border-color: var(--forest-green);
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.5rem;
        }

        .calendar-day-header {
            text-align: center;
            font-weight: 600;
            color: var(--text-light);
            padding: 0.5rem;
            font-size: 0.85rem;
        }

        .calendar-day {
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            cursor: pointer;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            background: var(--cream);
            color: var(--text-light);
            position: relative;
        }

        .calendar-day.has-data {
            background: white;
            color: var(--text-dark);
            border: 2px solid var(--sage);
            font-weight: 600;
        }

        .calendar-day.has-data:hover {
            background: var(--forest-green);
            color: white;
            border-color: var(--forest-green);
            transform: scale(1.05);
        }

        .calendar-day.selected {
            background: var(--dark-green);
            color: white;
            border-color: var(--dark-green);
        }

        .calendar-day.other-month {
            opacity: 0.3;
        }

        .calendar-day.has-data::after {
            content: '';
            position: absolute;
            bottom: 4px;
            width: 4px;
            height: 4px;
            background: var(--forest-green);
            border-radius: 50%;
        }

        .calendar-day.selected::after {
            background: white;
        }

        .time-picker {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 2px solid var(--cream);
        }

        .time-label {
            font-weight: 600;
            color: var(--dark-green);
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }

        .time-slots {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 0.5rem;
            max-height: 300px;
            overflow-y: auto;
            padding: 0.5rem;
        }

        .time-slot {
            background: var(--cream);
            border: 2px solid var(--sage);
            border-radius: 10px;
            padding: 0.8rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', monospace;
            font-size: 0.9rem;
        }

        .time-slot:hover {
            background: var(--forest-green);
            color: white;
            border-color: var(--forest-green);
        }

        .time-slot.selected {
            background: var(--dark-green);
            color: white;
            border-color: var(--dark-green);
        }

        .time-slot .temp-preview {
            font-size: 0.75rem;
            margin-top: 0.3rem;
            opacity: 0.8;
        }

        .confirm-selection {
            margin-top: 1.5rem;
            display: flex;
            justify-content: center;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2.5rem;
            }

            .temp-value {
                font-size: 4rem;
            }

            .plants-grid {
                grid-template-columns: 1fr;
            }

            .calendar-grid {
                gap: 0.3rem;
            }

            .calendar-day {
                font-size: 0.85rem;
            }

            .time-slots {
                grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌿 Plant Risk Monitor</h1>
            <p class="subtitle">Temperature-based plant health assessment</p>
        </header>

        <div class="calendar-container">
            <div class="calendar-header">
                <div class="calendar-month" id="calendarMonth">January 2026</div>
                <div class="calendar-nav">
                    <button class="nav-btn" onclick="previousMonth()">‹</button>
                    <button class="nav-btn" onclick="nextMonth()">›</button>
                </div>
            </div>

            <div class="calendar-grid" id="calendarGrid">
                <!-- Calendar will be generated here -->
            </div>

            <div class="time-picker" id="timePicker" style="display: none;">
                <div class="time-label">Select Time (Available readings marked)</div>
                <div class="time-slots" id="timeSlots">
                    <!-- Time slots will be generated here -->
                </div>
                <div class="confirm-selection">
                    <button onclick="confirmSelection()" id="confirmBtn" disabled>Select This Reading</button>
                </div>
            </div>
        </div>

        <div id="temperatureDisplay" class="temperature-display" style="display: none;">
            <div class="temp-label">Current Temperature Reading</div>
            <div class="temp-value" id="tempValue">--°C</div>
            <div class="temp-timestamp" id="tempTimestamp">No data selected</div>
        </div>

        <div class="plants-grid" id="plantsGrid">
            <div class="empty-state">
                <div class="empty-icon">🪴</div>
                <p>No plants added yet. Click "Add Plant" to start monitoring.</p>
            </div>
        </div>

        <div class="add-plant-btn" onclick="openModal()">
            <div class="add-icon">+</div>
            <div class="add-text">Add Plant</div>
        </div>
    </div>

    <div id="plantModal" class="modal">
        <div class="modal-content">
            <h2 class="modal-title">Add New Plant</h2>
            <form id="plantForm" onsubmit="addPlant(event)">
                <div class="form-group">
                    <label class="form-label">Plant Name *</label>
                    <input type="text" id="plantName" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Scientific Name</label>
                    <input type="text" id="plantScientific">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea id="plantDescription"></textarea>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Image URL (or emoji)</label>
                    <input type="text" id="plantImage" placeholder="🌱">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Minimum Safe Temperature (°C) *</label>
                    <input type="number" id="plantMinTemp" step="0.1" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Maximum Safe Temperature (°C) *</label>
                    <input type="number" id="plantMaxTemp" step="0.1" required>
                </div>
                
                <div class="button-group">
                    <button type="button" class="btn-cancel" onclick="closeModal()">Cancel</button>
                    <button type="submit">Add Plant</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Actual sensor data from Python
        let allData = DATA_PLACEHOLDER;
        let plants = JSON.parse(localStorage.getItem('plants') || '[]');
        let currentTemp = null;
        let currentMonth = new Date();
        let selectedDate = null;
        let selectedReading = null;

        // Group data by date
        function groupDataByDate() {
            const grouped = {};
            allData.forEach(record => {
                if (record.object_data.temperature !== undefined) {
                    const date = new Date(record.time);
                    const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
                    if (!grouped[dateKey]) {
                        grouped[dateKey] = [];
                    }
                    grouped[dateKey].push(record);
                }
            });
            return grouped;
        }

        const dataByDate = groupDataByDate();

        function renderCalendar() {
            const year = currentMonth.getFullYear();
            const month = currentMonth.getMonth();
            
            // Update month display
            const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December'];
            document.getElementById('calendarMonth').textContent = `${monthNames[month]} ${year}`;

            // Get first day of month and number of days
            const firstDay = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            const daysInPrevMonth = new Date(year, month, 0).getDate();

            const grid = document.getElementById('calendarGrid');
            grid.innerHTML = '';

            // Add day headers
            const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            dayHeaders.forEach(day => {
                const header = document.createElement('div');
                header.className = 'calendar-day-header';
                header.textContent = day;
                grid.appendChild(header);
            });

            // Add previous month days
            for (let i = firstDay - 1; i >= 0; i--) {
                const day = daysInPrevMonth - i;
                const dayEl = createDayElement(day, month - 1, year, true);
                grid.appendChild(dayEl);
            }

            // Add current month days
            for (let day = 1; day <= daysInMonth; day++) {
                const dayEl = createDayElement(day, month, year, false);
                grid.appendChild(dayEl);
            }

            // Add next month days to fill grid
            const remainingCells = 42 - (firstDay + daysInMonth);
            for (let day = 1; day <= remainingCells; day++) {
                const dayEl = createDayElement(day, month + 1, year, true);
                grid.appendChild(dayEl);
            }
        }

        function createDayElement(day, month, year, isOtherMonth) {
            const dayEl = document.createElement('div');
            dayEl.className = 'calendar-day';
            dayEl.textContent = day;

            if (isOtherMonth) {
                dayEl.classList.add('other-month');
            }

            // Check if this date has data
            const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            if (dataByDate[dateKey]) {
                dayEl.classList.add('has-data');
                dayEl.onclick = () => selectDate(year, month, day);
            }

            // Check if selected
            if (selectedDate && 
                selectedDate.getDate() === day && 
                selectedDate.getMonth() === month && 
                selectedDate.getFullYear() === year) {
                dayEl.classList.add('selected');
            }

            return dayEl;
        }

        function selectDate(year, month, day) {
            selectedDate = new Date(year, month, day);
            selectedReading = null;
            renderCalendar();
            showTimePicker();
        }

        function showTimePicker() {
            const dateKey = `${selectedDate.getFullYear()}-${String(selectedDate.getMonth() + 1).padStart(2, '0')}-${String(selectedDate.getDate()).padStart(2, '0')}`;
            const readings = dataByDate[dateKey] || [];

            const timePicker = document.getElementById('timePicker');
            const timeSlots = document.getElementById('timeSlots');
            
            if (readings.length === 0) {
                timePicker.style.display = 'none';
                return;
            }

            timePicker.style.display = 'block';
            timeSlots.innerHTML = '';

            readings.sort((a, b) => new Date(a.time) - new Date(b.time));

            readings.forEach((reading, index) => {
                const time = new Date(reading.time);
                const slot = document.createElement('div');
                slot.className = 'time-slot';
                
                const timeStr = time.toLocaleTimeString('en-US', { 
                    hour: '2-digit', 
                    minute: '2-digit',
                    hour12: true
                });
                
                const temp = reading.object_data.temperature;
                slot.innerHTML = `
                    <div>${timeStr}</div>
                    <div class="temp-preview">${temp.toFixed(1)}°C</div>
                `;
                
                slot.onclick = () => selectReading(reading, slot);
                timeSlots.appendChild(slot);
            });
        }

        function selectReading(reading, slotElement) {
            selectedReading = reading;
            
            // Update UI
            document.querySelectorAll('.time-slot').forEach(slot => {
                slot.classList.remove('selected');
            });
            slotElement.classList.add('selected');
            
            document.getElementById('confirmBtn').disabled = false;
        }

        function confirmSelection() {
            if (!selectedReading) return;

            currentTemp = selectedReading.object_data.temperature;
            
            // Display temperature
            document.getElementById('temperatureDisplay').style.display = 'block';
            document.getElementById('tempValue').textContent = currentTemp.toFixed(1) + '°C';
            document.getElementById('tempTimestamp').textContent = 
                'Recorded: ' + formatDate(selectedReading.time);

            // Update plant risk assessments
            renderPlants();

            // Scroll to temperature display
            document.getElementById('temperatureDisplay').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }

        function previousMonth() {
            currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1, 1);
            renderCalendar();
        }

        function nextMonth() {
            currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 1);
            renderCalendar();
        }

        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }

        function calculateDanger(plant, temp) {
            if (temp === null) return { level: 'unknown', label: 'Unknown' };
            
            const minTemp = parseFloat(plant.minTemp);
            const maxTemp = parseFloat(plant.maxTemp);
            
            if (temp >= minTemp && temp <= maxTemp) {
                return { level: 'low', label: 'Safe' };
            }
            
            const belowMin = minTemp - temp;
            const aboveMax = temp - maxTemp;
            const maxDeviation = Math.max(belowMin, aboveMax);
            
            if (maxDeviation <= 2) {
                return { level: 'moderate', label: 'Caution' };
            } else if (maxDeviation <= 5) {
                return { level: 'high', label: 'Warning' };
            } else {
                return { level: 'critical', label: 'Critical' };
            }
        }

        function renderPlants() {
            const grid = document.getElementById('plantsGrid');
            
            if (plants.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">🪴</div>
                        <p>No plants added yet. Click "Add Plant" to start monitoring.</p>
                    </div>
                `;
                return;
            }

            grid.innerHTML = plants.map((plant, index) => {
                const danger = calculateDanger(plant, currentTemp);
                const isImage = plant.image && (plant.image.startsWith('http') || plant.image.startsWith('data:'));
                
                return `
                    <div class="plant-card">
                        <div class="plant-image">
                            ${isImage ? 
                                `<img src="${plant.image}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.style.display='none'; this.parentElement.innerHTML='🌿'">` : 
                                plant.image || '🌿'
                            }
                        </div>
                        <span class="danger-badge danger-${danger.level}">${danger.label}</span>
                        <div class="plant-content">
                            <h3 class="plant-name">${plant.name}</h3>
                            ${plant.scientific ? `<div class="plant-scientific">${plant.scientific}</div>` : ''}
                            ${plant.description ? `<p class="plant-details">${plant.description}</p>` : ''}
                            <div class="temp-range">
                                <div class="temp-range-label">Safe Temperature Range</div>
                                <div>${plant.minTemp}°C - ${plant.maxTemp}°C</div>
                            </div>
                            ${currentTemp !== null ? `
                                <div class="temp-range" style="background: ${getDangerColor(danger.level)}15;">
                                    <div class="temp-range-label">Current Status</div>
                                    <div>${getDangerMessage(plant, currentTemp, danger.level)}</div>
                                </div>
                            ` : ''}
                            <button class="delete-btn" onclick="deletePlant(${index})">Delete Plant</button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function getDangerColor(level) {
            const colors = {
                low: '#2d5f3d',
                moderate: '#e6934e',
                high: '#c86b4a',
                critical: '#d64545',
                unknown: '#6b6b6b'
            };
            return colors[level] || colors.unknown;
        }

        function getDangerMessage(plant, temp, level) {
            const minTemp = parseFloat(plant.minTemp);
            const maxTemp = parseFloat(plant.maxTemp);
            
            if (level === 'low') {
                return '✓ Plant is within safe temperature range';
            } else if (temp < minTemp) {
                const diff = (minTemp - temp).toFixed(1);
                return `⚠️ Too cold by ${diff}°C`;
            } else {
                const diff = (temp - maxTemp).toFixed(1);
                return `⚠️ Too hot by ${diff}°C`;
            }
        }

        function openModal() {
            document.getElementById('plantModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('plantModal').classList.remove('active');
            document.getElementById('plantForm').reset();
        }

        function addPlant(event) {
            event.preventDefault();
            
            const plant = {
                name: document.getElementById('plantName').value,
                scientific: document.getElementById('plantScientific').value,
                description: document.getElementById('plantDescription').value,
                image: document.getElementById('plantImage').value || '🌿',
                minTemp: document.getElementById('plantMinTemp').value,
                maxTemp: document.getElementById('plantMaxTemp').value
            };

            plants.push(plant);
            localStorage.setItem('plants', JSON.stringify(plants));
            
            closeModal();
            renderPlants();
        }

        function deletePlant(index) {
            if (confirm('Are you sure you want to delete this plant?')) {
                plants.splice(index, 1);
                localStorage.setItem('plants', JSON.stringify(plants));
                renderPlants();
            }
        }

        // Initial render
        renderCalendar();
        renderPlants();
    </script>
</body>
</html>'''

# Convert sensor data to JSON and embed in HTML
data_json = json.dumps(sensor_data_list, indent=2)
html_content = html_template.replace('DATA_PLACEHOLDER', data_json)

# Write HTML file
output_file = 'plant_risk_monitor.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\nHTML file generated successfully: {output_file}")
print(f"Open this file in your web browser to use the Plant Risk Monitor.")