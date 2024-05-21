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
    const jsonResponse = sendJsonPayload(url, payload);
    return jsonResponse;
}

async function get_client_list(url) {
    //Ved ik om server url er statisk eller om vi skal lave den dynamisk.
    const payload = {
        type: 'clients',
        query: 'get_list',
    };
    const jsonResponse = sendJsonPayload(url, payload);
    return jsonResponse;
    //logic for adding json response to frontend goes here.
}

function add_client() {
    //Is this just locally or also added to server's list?
}

function delete_client() {
    //Is this just locally or also deleted from server's list?
}

async function get_stats(url) {
    const payload = {
        type: 'statistics',
        query: 'get_stats',
    };
    const jsonResponse = sendJsonPayload(url, payload);
    return jsonResponse;
}

async function start_server(url) {
    const payload = {
        type: 'server',
        query: 'server_start',
    };
    const jsonResponse = sendJsonPayload(url, payload);
    return jsonResponse;
}

async function stop_server(url) {
    const payload = {
        type: 'server',
        query: 'server_stop',
    };
    const jsonResponse = sendJsonPayload(url, payload);
    return jsonResponse;
}

function get_server_status(url) {
    const payload = {
        type: 'server',
        query: 'server_status',
    };
    const jsonResponse = sendJsonPayload(url, payload);
    return jsonResponse;
}