async function loadAlerts() {
    const res = await fetch('fssai_data.json');
    const data = await res.json();
    const list = document.getElementById('fssaiList');
    
    if (data.length === 0) {
        list.innerHTML = "<p>No new alerts found today.</p>";
        return;
    }

    list.innerHTML = data.map(item => `
        <div class="card">
            <small>${item.date}</small>
            <h3>${item.title}</h3>
            <a href="${item.url}" target="_blank">View Circular (PDF)</a>
        </div>
    `).join('');
}
loadAlerts();
