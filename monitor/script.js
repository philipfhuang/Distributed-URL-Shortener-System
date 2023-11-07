document.addEventListener("DOMContentLoaded", () => {
    getNodeInfo(); // Fetch initially
    setInterval(getNodeInfo, 5000); // Fetch every 5 seconds
});

function getNodeInfo() {
    fetch('/get_docker_nodes') // Replace this with your actual endpoint to get Docker node info from the backend
        .then(response => response.json())
        .then(data => updateNodesTable(data))
        .catch(error => console.error('Error:', error));
}

function updateNodesTable(nodes) {
    const nodesInfoContainer = document.getElementById('nodesInfo');
    nodesInfoContainer.innerHTML = ''; // Clear previous content

    nodes.forEach(node => {
        const row = document.createElement('tr');

        Object.keys(node).forEach(key => {
            const cell = document.createElement('td');
            cell.textContent = node[key];
            if (key === 'status') {
                const statusValue = node[key].toLowerCase();
                console.log(statusValue);
                if (statusValue.includes('unhealthy')) {
                    cell.classList.add('status-unhealthy');
                } else if (statusValue.includes('up')) {
                    cell.classList.add('status-up');
                } else {
                    cell.classList.add('status-other');
                }
            }
            row.appendChild(cell);
        });

        nodesInfoContainer.appendChild(row);
    });
}
