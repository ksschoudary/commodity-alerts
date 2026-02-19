async function loadPIB() {
    const res = await fetch('pib_data.json');
    const data = await res.json();
    const container = document.getElementById('pibList');
    
    container.innerHTML = data.map(item => `
        <div class="pib-card">
            <div class="aging-badge">${item.aging}</div>
            <div class="pib-date">${item.date}</div>
            <h3 class="pib-title">${item.title}</h3>
            <a href="${item.url}" target="_blank" class="pib-link">View Official Release</a>
        </div>
    `).join('');
}
loadPIB();
