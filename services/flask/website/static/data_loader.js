document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('data-container');
    if (!container) return;

    const endpoint = container.getAttribute('data-endpoint');
    if(!endpoint) {
        container.innerText = 'No data endpoint provided.';
        return;
    }

    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            if (!data.items || data.items.length === 0) {
                container.innerText = 'No data found.'
                return;
            }
            const table = document.createElement('table');
            table.className = "table table-striped";

            // Create header from keys of the first item
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            Object.keys(data.items[0]).forEach(key => {
                const th = document.createElement('th');
                th.innerText = key;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            const tbody = document.createElement('tbody');
            data.items.forEach(item => {
                const row = document.createElement('tr');
                Object.values(item).forEach(value => {
                    const td = document.createElement('td');
                    td.innerText = value;
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });
            table.appendChild(tbody);

            container.innerHTML = '';
            container.appendChild(table);
        })
        .catch(error => {
            container.innerText = 'Error loading data: ' + error.message;
            console.error('Fetch error:', error);
        });
});