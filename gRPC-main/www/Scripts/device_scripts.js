document.addEventListener('DOMContentLoaded', function() {
    const clientId = sessionStorage.getItem('clientId');
    console.log('Interacting with device:', clientId);

    document.getElementById('start_stream_button').addEventListener('click', () => {
        fetch('http://homeassistant.local:5000/start_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: clientId })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Start Stream Response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('stop_stream_button').addEventListener('click', () => {
        fetch('http://homeassistant.local:5000/stop_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: clientId })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Stop Stream Response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    document.getElementById('get_alert_screenshots_button').addEventListener('click', () => {
        fetch('http://homeassistant.local:5000/retrieve_frames', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: clientId })
        })
        .then(response => response.json())
        .then(data => {
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
            console.error('Error:', error);
        });
    });

    // Load initial alerts
    loadAlerts(clientId);
});

async function loadAlerts(clientId) {
    try {
        const response = await fetch(`http://homeassistant.local:5000/alerts?client_id=${clientId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to load alerts: ${response.status}`);
        }

        const data = await response.json();
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
