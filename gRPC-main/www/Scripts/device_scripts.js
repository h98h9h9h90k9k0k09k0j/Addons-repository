document.addEventListener('DOMContentLoaded', function() {
    const clientId = sessionStorage.getItem('clientId');
    console.log('Interacting with device:', clientId);

    document.getElementById('start_stream_button').addEventListener('click', () => {
        console.log('Starting stream with clientId:', clientId);
        fetch('http://homeassistant.local:5000/start_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: clientId, processing_mode: document.getElementById('processing_mode').value })
        })
        .then(response => {
            if (!response.ok) {
                console.error('Failed to start stream, status:', response.status);
                throw new Error(`Failed to start stream: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Start Stream Response:', data);
        })
        .catch(error => {
            console.error('Error starting stream:', error);
        });
    });

    document.getElementById('stop_stream_button').addEventListener('click', () => {
        console.log('Stopping stream with clientId:', clientId);
        fetch('http://homeassistant.local:5000/stop_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: clientId })
        })
        .then(response => {
            if (!response.ok) {
                console.error('Failed to stop stream, status:', response.status);
                throw new Error(`Failed to stop stream: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Stop Stream Response:', data);
        })
        .catch(error => {
            console.error('Error stopping stream:', error);
        });
    });

    document.getElementById('get_alert_screenshots_button').addEventListener('click', () => {
        console.log('Fetching alert screenshots for clientId:', clientId);
        fetch('http://homeassistant.local:5000/retrieve_frames', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: clientId })
        })
        .then(response => {
            if (!response.ok) {
                console.error('Failed to retrieve frames, status:', response.status);
                throw new Error(`Failed to retrieve frames: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Alert screenshots fetched:', data);
            const alertScreenshotsDiv = document.getElementById('alert_screenshots');
            alertScreenshotsDiv.innerHTML = ''; // Clear existing screenshots

            data.frames.forEach(frame => {
                const img = document.createElement('img');
                img.src = `data:image/jpeg;base64,${frame}`;
                img.alt = 'Alert Screenshot';
                alertScreenshotsDiv.appendChild(img);
            });
        })
        .catch(error => {
            console.error('Error fetching alert screenshots:', error);
        });
    });

    // Load initial alerts
    loadAlerts(clientId);

    // Poll for alerts every 10 seconds
    setInterval(() => {
        loadAlerts(clientId);
    }, 10000);
});

async function loadAlerts(clientId) {
    console.log('Loading alerts for clientId:', clientId);
    try {
        const response = await fetch(`http://homeassistant.local:5000/alerts?client_id=${clientId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Failed to load alerts, status:', response.status);
            throw new Error(`Failed to load alerts: ${response.status}`);
        }

        const data = await response.json();
        console.log('Alerts loaded:', data);
        const alertsDiv = document.getElementById('alerts');
        alertsDiv.innerHTML = ''; // Clear existing alerts

        data.alerts.forEach(alert => {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert';
            alertDiv.textContent = alert.message;
            alertsDiv.appendChild(alertDiv);
        });
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}
