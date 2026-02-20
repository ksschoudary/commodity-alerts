const DATA_SOURCES = {
    wheat: 'wheat_news.json',
    pib: 'pib_data.json',
    reg: 'fssai_data.json'
};

async function switchSegment(segment) {
    const container = document.getElementById('main-feed');
    console.log("Switching to:", segment);

    // Update UI
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.querySelector(`[data-segment="${segment}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    container.innerHTML = `<div style="padding:20px; color:gray;">Loading ${segment}...</div>`;

    try {
        // Cache-buster: adding ?v= ensures we ignore old browser data
        const response = await fetch(`${DATA_SOURCES[segment]}?v=${new Date().getTime()}`);
        if (!response.ok) throw new Error('File not found');
        
        const data = await response.json();
        console.log("Data loaded for " + segment, data);

        if (!data || data.length === 0) {
            container.innerHTML = `<div style="padding:20px;">No updates found in ${DATA_SOURCES[segment]}.</div>`;
            return;
        }

        renderFeed(data, segment);
    } catch (error) {
        console.error(error);
        container.innerHTML = `<div style="padding:20px; color:red;">Connection Error. Check GitHub Actions status.</div>`;
    }
}

function renderFeed(data, type) {
    const container = document.getElementById('main-feed');
    
    container.innerHTML = data.map(item => {
        // FLEXIBLE KEYS: This checks for both 'title' and 'Title'
        const title = item.title || item.Title || "No Title Available";
        const url = item.url || item.Link || item.url || "#";
        const date = item.aging || item.date || item.Date || "Recent";

        return `
            <div class="card" data-type="${type}">
                <div class="card-header">
                    <span class="badge">${date}</span>
                </div>
                <h3 class="card-title">${title}</h3>
                <div class="card-footer">
                    <a href="${url}" target="_blank" class="view-btn">View Official Release →</a>
                </div>
            </div>
        `;
    }).join('');
}
