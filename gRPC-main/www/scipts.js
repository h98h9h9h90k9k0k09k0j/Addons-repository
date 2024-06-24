document.getElementById('device-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const name = document.getElementById('device-name').value;
    const ip = document.getElementById('device-ip').value;
    const port = document.getElementById('device-port').value;

    const response = await fetch('http://localhost:5000/add_client', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: name, address: `${ip}:${port}` })
    });

    if (response.ok) {
        addDeviceToList(name, `${ip}:${port}`);
    }
});

async function addDeviceToList(name, address) {
    const deviceList = document.getElementById('device-list');
    const li = document.createElement('li');
    li.textContent = `${name} (${address})`;
    li.addEventListener('click', () => {
        window.location.href = `device.html?name=${name}&address=${address}`;
    });
    deviceList.appendChild(li);
}

// Fetch and display the list of devices when the page loads
async function loadDevices() {
    const response = await fetch('http://localhost:5000/list_clients');
    const data = await response.json();
    data.clients.forEach(client => {
        addDeviceToList(client.client_id, client.address);
    });
}

loadDevices();
