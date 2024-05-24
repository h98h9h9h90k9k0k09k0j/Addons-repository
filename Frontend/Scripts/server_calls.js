async function send_json_payload(url, payload) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const jsonResponse = await response.json();
        console.log('Server reponse:', jsonResponse);
        return jsonResponse;
    } catch (error) {
        console.error('Error:', error);
    }
}

function detection_selection() {
    const dropdown = document.getElementById('options');
    const selectedValue = dropdown.value;
    if (selectedValue == "none") {
        alert('Please choose a valid option');
        return;
    }
    const jsonResponse = send_json_payload(url, payload);
    return jsonResponse;
}

function list_clients() {
    //Erstat url med korrekte endpoint
    const url = 'http://homeassistant.local:5000/list_clients';
    
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function add_client(client_id, address) {
    //Erstat url med korrekte endpoint
    const url = 'http://homeassistant.local:5000/add_client';

    const data = {
        client_id: client_id,
        address: address
    };
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function delete_client(client_id) {
    //Erstat url med korrekte endpoint
    const url = 'http://homeassistant.local:5000/delete_client';

    const data = {
        client_id: client_id,
    };
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Client deleted:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

async function get_stats(url) {
    const payload = {
        type: 'statistics',
        query: 'get_stats',
    };
    const jsonResponse = send_json_payload(url, payload);
    return jsonResponse;
}

async function start_server(url) {
    const payload = {
        type: 'server',
        query: 'server_start',
    };
    const jsonResponse = send_json_payload(url, payload);
    return jsonResponse;
}

async function stop_server(url) {
    const payload = {
        type: 'server',
        query: 'server_stop',
    };
    const jsonResponse = send_json_payload(url, payload);
    return jsonResponse;
}

function get_server_status(url) {
    const payload = {
        type: 'server',
        query: 'server_status',
    };
    const jsonResponse = send_json_payload(url, payload);
    return jsonResponse;
}

document.getElementById('add_client_form').addEventListener('submit', function(event) {
    event.preventDefault();
    const client_id = document.getElementById('add_client_id').value;
    const address = document.getElementById('add_client_address').value;
    add_client(client_id, address);
});

document.getElementById('delete_client_form').addEventListener('submit', function(event) {
    event.preventDefault();
    const client_id = document.getElementById('delete_client_id').value;
    delete_client(client_id);
});

document.getElementById('list_clients_form').addEventListener('submit', function(event) {
    event.preventDefault();
    list_clients();
});