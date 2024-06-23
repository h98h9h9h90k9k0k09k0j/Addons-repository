const devices = [
    { name: 'Raspberry Pi', link: 'frontend2.html' },
    { name: 'Jetson Nano', link: 'frontend2.html' }
];

function addDevice(name, link) {
    const ul = document.getElementById('deviceList');
    const li = document.createElement('li');
    const a = document.createElement('a');
    const span = document.createElement('span');

    a.href = link;
    span.textContent = name;

    a.appendChild(span);
    li.appendChild(a);
    ul.appendChild(li);
}

function loadDevices() {
    devices.forEach(device => {
        addDevice(device.name, device.link);
    });
}

// Initial load
loadDevices();

// Example of adding a new device dynamically
addDevice('New Device', 'newdevice.html');