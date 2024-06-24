document.getElementById('add_device_form').addEventListener('submit', function(event) {
    event.preventDefault();
    const deviceId = document.getElementById('device_id').value;
    const deviceAddress = document.getElementById('device_address').value;
    addDevice(deviceId, deviceAddress);
});

async function loadDevices() {
    console.log('Entering loadDevices function');
    try {
        const response = await fetch('http://homeassistant.local:5000/list_clients', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Failed to load devices, status:', response.status);
            throw new Error(`Failed to load devices: ${response.status}`);
        }

        const data = await response.json();
        console.log('Devices loaded:', data);
        const devices = data.clients;

        const ul = document.getElementById('device_list');
        ul.innerHTML = ''; // Clear existing list

        devices.forEach(device => {
            addDeviceElement(device.client_id, 'device.html');
        });
    } catch (error) {
        console.error('Error loading devices:', error);
    }
}

async function addDevice(deviceId, deviceAddress) {
    console.log('Entering addDevice function with deviceId:', deviceId, 'and deviceAddress:', deviceAddress);
    try {
        const response = await fetch('http://homeassistant.local:5000/add_client', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ client_id: deviceId, address: deviceAddress })
        });

        if (!response.ok) {
            console.error('Failed to add device, status:', response.status);
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

function addDeviceElement(name, link) {
    console.log('Entering addDeviceElement function with name:', name, 'and link:', link);
    const ul = document.getElementById('device_list');
    const li = document.createElement('li');
    const a = document.createElement('a');
    const span = document.createElement('span');

    a.href = link;
    a.setAttribute('data-client-id', name); // Set a data attribute to pass client id to the new page
    a.addEventListener('click', function(event) {
        event.preventDefault();
        navigateTo(link, name);
    });
    span.textContent = name;

    a.appendChild(span);
    li.appendChild(a);
    ul.appendChild(li);
}

// Initial load
loadDevices();
