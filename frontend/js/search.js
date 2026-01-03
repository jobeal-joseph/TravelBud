const searchInput = document.getElementById('city-search');
const resultsDiv = document.getElementById('city-results');
const statusMsg = document.getElementById('status-msg');

searchInput.addEventListener('input', async (e) => {
    const query = e.target.value.trim();

    if (query.length < 3) {
        resultsDiv.innerHTML = '';
        return;
    }

    try {
        statusMsg.classList.remove('d-none');
        
        const response = await fetch(`/api/search/cities?q=${query}`);
        const cities = await response.json();

        statusMsg.classList.add('d-none');
        
        if (cities.length === 0) {
            resultsDiv.innerHTML = '<li class="list-group-item text-center">No cities found.</li>';
            return;
        }

        resultsDiv.innerHTML = cities.map(city => `
            <li class="list-group-item d-flex justify-content-between align-items-center py-3 city-card">
                <div>
                    <h6 class="mb-0 fw-bold">${city.city}</h6>
                    <small class="text-muted">${city.region}, ${city.country}</small>
                </div>
                <button class="btn btn-sm btn-outline-success rounded-pill" onclick="alert('Added ${city.city}!')">
                    Add to Trip
                </button>
            </li>
        `).join('');

    } catch (error) {
        console.error('Search failed:', error);
        statusMsg.innerHTML = '<p class="text-danger">Check your connection</p>';
    }
});