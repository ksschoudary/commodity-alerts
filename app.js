// Map to the files created by the Python script
const DATA_SOURCES = {
    wheat: 'wheat_news.json',
    pib: 'pib_data.json',
    reg: 'fssai_data.json'
};

document.addEventListener('DOMContentLoaded', () => switchSegment('wheat'));

async function switchSegment(segment) {
    const container = document.getElementById('main-feed');
    
    // UI Highlight
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.querySelector(`[data-segment="${segment}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    container.innerHTML = `<div style="padding:20px; color:#8b949e;">Syncing ${segment} pulse...</div>`;

    try {
        // The '?v=' forces a fresh pull from GitHub (No caching)
        const response = await fetch(`${DATA_SOURCES[segment]}?v=${new Date().getTime()}`);
        const data = await response.json();

        if (!data || data.length === 0) {
            container.innerHTML = `<div style="padding:20px;">No new updates found in ${segment}.</div>`;
            return;
        }

        renderFeed(data, segment);
    } catch (error) {
        container.innerHTML = `<div style="padding:20px; color:#e74c3c;">Connection Error. Run Scraper on GitHub.</div>`;
    }
}

function renderFeed(data, type) {
    const container = document.getElementById('main-feed');
    
    container.innerHTML = data.map(item => `
        <div class="card" data-type="${type}">
            <div class="card-header">
                <span class="badge">${item.aging || 'Latest'}</span>
                <span class="date-label">${item.date}</span>
            </div>
            <h3 class="card-title">${item.title}</h3>
            <div class="card-footer">
                <a href="${item.url}" target="_blank" class="view-btn">Read Official Release →</a>
            </div>
        </div>
    `).join('');
}
