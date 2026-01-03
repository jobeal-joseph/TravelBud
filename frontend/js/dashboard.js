fetch("/api/trips")
  .then(res => res.json())
  .then(data => {
    trips.innerHTML = data.map(t => `
      <div class="col-md-4">
        <div class="card mb-3">
          <div class="card-body">
            <h5>${t.name}</h5>
            <p>${t.start_date} → ${t.end_date}</p>
            <a href="/trip/${t.id}" class="btn btn-sm btn-outline-primary">View</a>
          </div>
        </div>
      </div>
    `).join("");
  });
