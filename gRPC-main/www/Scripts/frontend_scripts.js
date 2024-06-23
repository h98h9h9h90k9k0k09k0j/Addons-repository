async function loadDevices() {
    try {
        const response = await fetch('http://homeassistant.local:5000/list_clients', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to load devices: ${response.status}`);
        }

        const data = await response.json();
        const devices = data.clients;

        const ul = document.getElementById('deviceList');
        ul.innerHTML = ''; // Clear existing list

        devices.forEach(device => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            const span = document.createElement('span');

            a.href = 'frontend2.html'; // Adjust if needed
            span.textContent = device.client_id;

            a.appendChild(span);
            li.appendChild(a);
            ul.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading devices:', error);
    }
}

async function addDevice(client_id, address) {
    try {
        const response = await fetch('http://homeassistant.local:5000/add_client', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id, address })
        });

        if (!response.ok) {
            throw new Error(`Failed to add device: ${response.status}`);
        }

        const data = await response.json();
        console.log('Device added:', data);

        // Reload devices after adding a new one
        await loadDevices();
    } catch (error) {
        console.error('Error adding device:', error);
    }
}

document.getElementById('add_client_form').addEventListener('submit', function(event) {
    event.preventDefault();
    const client_id = document.getElementById('add_client_id').value;
    const address = document.getElementById('add_client_address').value;
    addDevice(client_id, address);
});

// Initial load
loadDevices();
