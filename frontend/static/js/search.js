const searchInput = document.getElementById('city-search');
const resultsDiv = document.getElementById('city-results');

searchInput.addEventListener('input', async (e) => {
    const query = e.target.value;
    if (query.length < 3) return;

    const res = await fetch(`/api/cities?q=${query}`);
    const cities = await res.json();

    resultsDiv.innerHTML = cities.map(c => `
        <div class="col-md-4">
            <div class="card city-card h-100 shadow-sm">
                <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=400&q=60&sig=${Math.random()}" class="city-img">
                <div class="card-body p-4">
                    <h5 class="fw-bold mb-1">${c.city}</h5>
                    <p class="text-muted small mb-3">${c.country}</p>
                    <button class="btn btn-primary w-100 rounded-pill py-2 fw-bold" onclick="saveTrip('${c.city}', '${c.country}')">Plan Budget</button>
                </div>
            </div>
        </div>
    `).join('');
});

async function saveTrip(city, country) {
    const res = await fetch('/api/trips/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ city, country })
    });
    const data = await res.json();
    if(res.ok) {
        localStorage.setItem('trip_id', data.trip_id);
        localStorage.setItem('city_name', city);
        window.location.href = '/budget';
    }
}