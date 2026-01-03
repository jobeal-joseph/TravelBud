document.getElementById('city-search').addEventListener('input', async (e) => {
    const query = e.target.value;
    if (query.length < 3) return;
    const res = await fetch(`/api/cities?q=${query}`);
    const cities = await res.json();
    document.getElementById('city-results').innerHTML = cities.map(c => `
        <div class="col-md-4">
            <div class="card city-card p-3">
                <h5 class="fw-bold">${c.city}</h5>
                <p class="small text-muted">${c.country}</p>
                <button class="btn btn-sm btn-primary" onclick="location.href='/budget'">Plan Budget</button>
            </div>
        </div>
    `).join('');
});