

// Function to dynamically create and display the list of entities
function display_entities(entity_array) {
    const entity_list = document.getElementById('entity_list');
    entity_list.innerHTML = '';

    entity_array.forEach(entity => {
        const list_item = document.createElement('li');
        list_item.textContent = `Name: ${entity.name}`;
        entity_list.appendChild(list_item);
    });
}

document.getElementById('startStreamButton').addEventListener('click', () => {
    //Server Url Goes Here
    fetch('http://your-server-url/start-stream', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Start Stream Response:', data);
        // Handle success or error response here
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

document.getElementById('stopStreamButton').addEventListener('click', () => {
    //Server Url Goes Here
    fetch('http://your-server-url/stop-stream', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Stop Stream Response:', data);
        // Handle success or error response here
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

document.getElementById('toggleCheckbox').addEventListener('change', function() {
    var toggleDiv = document.querySelector('.toggleDiv');
    if (this.checked) {
        toggleDiv.style.display = 'block';
    } else {
        toggleDiv.style.display = 'none';
    }
});

document.getElementById('toggleScreenshot').addEventListener('change', function() {
    var notificationImage = document.getElementById('notificationImage');
    if (this.checked) {
        notificationImage.style.display = 'block';
    } else {
        notificationImage.style.display = 'none';
    }
});