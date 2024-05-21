// Get the canvas element
const ctx = document.getElementById('performance_chart').getContext('2d');

// Define the data for server and client metrics
const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
        label: 'Server Performance',
        data: [100, 120, 110, 105, 115, 130],
        borderColor: 'rgba(255, 99, 132, 1)', // Red color
        borderWidth: 2,
        fill: false
    }, {
        label: 'Client Performance',
        data: [90, 100, 95, 105, 110, 120],
        borderColor: 'rgba(54, 162, 235, 1)', // Blue color
        borderWidth: 2,
        fill: false
    }]
};

// Create the chart
const performance_chart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: {
        responsive: false, // Disable responsiveness for fixed size
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});