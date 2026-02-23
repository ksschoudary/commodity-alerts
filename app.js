const DATA_SOURCES = {
    wheat: 'wheat_news.json',
    pib: 'pib_data.json',
    reg: 'fssai_data.json'
};

// 1. Initial Load
document.addEventListener('DOMContentLoaded', () => {
    switchSegment('wheat');
});

// 2. Main Navigation Function
async function switchSegment(segment) {
    const container = document.getElementById('main-feed');
    
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.querySelector(`[data-segment="${segment}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    container.innerHTML = `<div class="spinner"></div><p style="text-align:center;color:gray;">Syncing ${segment}...</p>`;

    try {
        const response = await fetch(`${DATA_SOURCES[segment]}?v=${Date.now()}`);
        const wrapper = await response.json();
        
        // Extract news and sync time from your new JSON structure
        const data = wrapper.news || [];
        const lastSync = wrapper.sync_time || "Recent";

        const statusEl = document.querySelector('.status-indicator');
        if (statusEl) statusEl.innerHTML = `<span class="dot"></span> Live Pulse: ${lastSync}`;

        if (!data || data.length === 0) {
            container.innerHTML = `<div style="padding:20px; text-align:center;">No fresh updates found.</div>`;
            return;
        }

        renderFeed(data, segment);
    } catch (error) {
        console.error("Fetch Error:", error);
        container.innerHTML = `<div style="padding:20px; color:red; text-align:center;">Sync Error. Check GitHub Actions.</div>`;
    }
}

// 3. Rendering Engine
function renderFeed(data, type) {
    const container = document.getElementById('main-feed');
    container.innerHTML = data.map(item => `
        <div class="card" data-type="${type}">
            <div class="card-header">
                <span class="badge">Latest</span>
                <span class="date-label">${item.date || 'Recent'}</span>
            </div>
            <h3 class="card-title">${item.title}</h3>
            <div class="card-footer">
                <a href="${item.url}" target="_blank" class="view-btn">Read Official Release →</a>
            </div>
        </div>
    `).join('');
}

// 4. THE FIX: The Emergency Reset Function (Must be top-level)
async function emergencyReset() {
    const btn = document.getElementById('refresh-btn');
    if (btn) btn.innerText = "Purging...";

    try {
        // Clear Caches
        if ('caches' in window) {
            const keys = await caches.keys();
            await Promise.all(keys.map(key => caches.delete(key)));
        }

        // Unregister Service Workers
        if ('serviceWorker' in navigator) {
            const registrations = await navigator.serviceWorker.getRegistrations();
            for (let reg of registrations) {
                await reg.unregister();
            }
        }

        // Hard Reload
        window.location.href = window.location.origin + window.location.pathname + '?bust=' + Date.now();
    } catch (e) {
        console.error("Reset failed", e);
        window.location.reload(true);
    }
}
