const urlParams = new URLSearchParams(window.location.search);
const deviceName = urlParams.get('name');
const deviceAddress = urlParams.get('address');
const deviceTitle = document.getElementById('device-title');
deviceTitle.textContent = `${deviceName} (${deviceAddress})`;

document.getElementById('processing-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const processingType = document.getElementById('processing-type').value;

    const response = await fetch('http://localhost:5000/start_stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: deviceName, task_id: processingType })
    });

    if (response.ok) {
        fetchAlerts();
    }
});

async function fetchAlerts() {
    const response = await fetch('http://localhost:5000/alerts');
    const data = await response.json();
    const alertsList = document.getElementById('alerts-list');
    alertsList.innerHTML = '';
    data.alerts.forEach(alert => {
        const li = document.createElement('li');
        li.textContent = alert;
        alertsList.appendChild(li);
    });
}

document.getElementById('fetch-screenshots').addEventListener('click', async function() {
    const response = await fetch('http://localhost:5000/retrieve_frames', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: deviceName })
    });

    if (response.ok) {
        const data = await response.json();
        const screenshotsContainer = document.getElementById('screenshots-container');
        screenshotsContainer.innerHTML = '';
        data.frames.forEach(frame => {
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64,${frame}`;
            screenshotsContainer.appendChild(img);
        });
    }
});

// Regularly fetch alerts every 10 seconds
setInterval(fetchAlerts, 10000);
