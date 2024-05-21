// Array of entity objects with name and unique ID
const entities = [
    { name: 'Client One' },
    { name: 'Client Two' },
    { name: 'Client Three' },
    { name: 'Client Four' },
    { name: 'Client Five' }
];

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

function add_entity() {
    const input_field = document.getElementById('entity_input');
    const entityName = input_field.value.trim();

    //Change this to save entries to whatever list holds clients
    if (entityName) {
        const newId = entities.length > 0 ? entities[entities.length - 1].id + 1 : 1;
        const newEntity = { id: newId, name: entityName };
        entities.push(newEntity);
        display_entities(entities);
        input_field.value = '';
    } else {
        alert('Please enter a valid entity name.');
    }
}

function start_server() {
    alert('Server is now starting');
    //Logic to start server here.
}

function stop_server() {
    alert('Server is now stopping');
    //Logic to stop server here.
}

function toggle_dots() {
    const dot_containers = document.querySelectorAll('.dot-container');
    //Code for changing status here, add a trigger.
    dot_containers.forEach(container => {
        const dot = container.querySelector('.dot');
        const description = container.querySelector('.description');

        if (dot.classList.contains('off')) {
            dot.classList.remove('off');
            dot.classList.add('on');
            description.textContent = description.textContent.replace('Off', 'On');
        } else {
            dot.classList.remove('on');
            dot.classList.add('off');
            description.textContent = description.textContent.replace('On', 'Off');
        }
    });
}

document.getElementById('fileInput').addEventListener('change', readFile);

function readFile(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            displayNames(data.users);
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    };
    reader.readAsText(file);
}

function displayNames(users) {
    const nameList = document.getElementById('nameList');
    nameList.innerHTML = ''; // Clear any existing content
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = user.name;
        nameList.appendChild(li);
    });
}





// Call the function to display the entities
display_entities(entities);
