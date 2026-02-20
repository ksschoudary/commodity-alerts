/**
 * MASTER APP ENGINE: Commodity Intelligence Tracker
 * Segments: Wheat News, PIB Updates, Regulatory
 */

// 1. DATA CONFIGURATION
const DATA_SOURCES = {
    wheat: 'wheat_news.json',
    pib: 'pib_data.json',
    reg: 'fssai_data.json'
};

// 2. INITIALIZE ON LOAD
document.addEventListener('DOMContentLoaded', () => {
    // Default to 'wheat' segment on startup
    switchSegment('wheat');
});

/**
 * CORE LOGIC: Switch between segments and fetch data
 * Includes "Cache-Buster" and "No-Store" headers to prevent old data display
 */
async function switchSegment(segment) {
    const container = document.getElementById('main-feed');
    // ... (UI highlight code remains same)

    try {
        const response = await fetch(`${DATA_SOURCES[segment]}?v=${Date.now()}`);
        const wrapper = await response.json();
        
        // Handle the new structure {sync_time: "...", news: [...]}
        const data = wrapper.news || [];
        const lastSync = wrapper.sync_time || "Updating...";

        // Update the header with the Last Updated timestamp
        const statusEl = document.querySelector('.status-indicator');
        if (statusEl) statusEl.innerHTML = `<span class="dot"></span> Last Sync: ${lastSync}`;

        if (!data || data.length === 0) {
            container.innerHTML = `<div class="empty-state">No fresh updates found.</div>`;
            return;
        }

        renderFeed(data, segment);
    } catch (error) {
        console.error(error);
    }
}
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        const data = await response.json();
        console.log(`Data for ${segment}:`, data);

        if (!data || data.length === 0) {
            container.innerHTML = `
                <div style="padding:40px; text-align:center; color:#8b949e;">
                    <p>No recent ${segment} updates found.</p>
                    <p style="font-size:0.8rem;">Check GitHub Actions logs for sync status.</p>
                </div>`;
            return;
        }

        renderFeed(data, segment);

    } catch (error) {
        console.error("Fetch Failure:", error);
        container.innerHTML = `
            <div style="padding:40px; text-align:center; color:#e74c3c;">
                <p><strong>Connection Interrupted</strong></p>
                <p style="font-size:0.8rem; color:#8b949e;">${error.message}</p>
            </div>`;
    }
}

/**
 * RENDERING ENGINE: Converts JSON to visual cards
 * Uses Flexible Key Matching for robust data display
 */
function renderFeed(data, type) {
    const container = document.getElementById('main-feed');
    
    const html = data.map(item => {
        // FLEXIBLE KEY MATCHING: Handles both 'title' and 'Title' etc.
        const title = item.title || item.Title || "Untitled Release";
        const url = item.url || item.Link || item.url || "#";
        const date = item.date || item.Date || item.published || "Recent";
        const aging = item.aging || "Latest Update";

        // Segment-Specific Branding
        const sourceLabel = type === 'wheat' ? 'Market Feed' : (type === 'pib' ? 'PIB India' : 'FSSAI Regulatory');

        return `
            <div class="card" data-type="${type}">
                <div class="card-header">
                    <span class="badge">${aging}</span>
                    <span class="source-label">${sourceLabel}</span>
                </div>
                <h3 class="card-title">${title}</h3>
                <div class="card-subtitle">${date}</div>
                <div class="card-footer">
                    <a href="${url}" target="_blank" class="view-btn">View Official Release →</a>
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}

/**
 * NUCLEAR RESET: Bypasses Service Worker & Browser Cache
 * Use this when the app feels "stuck"
 */
async function emergencyReset() {
    const btn = document.getElementById('refresh-btn');
    if(btn) {
        btn.innerText = "Purging Cache...";
        btn.style.opacity = "0.5";
    }

    try {
        // 1. Clear Service Worker Cache
        if ('caches' in window) {
            const keys = await caches.keys();
            await Promise.all(keys.map(key => caches.delete(key)));
        }

        // 2. Unregister Service Workers
        if ('serviceWorker' in navigator) {
            const registrations = await navigator.serviceWorker.getRegistrations();
            for (let reg of registrations) {
                await reg.unregister();
            }
        }

        // 3. Wipe Storage
        localStorage.clear();
        sessionStorage.clear();

        // 4. Forced Hard Reload with Timestamp
        window.location.href = window.location.origin + window.location.pathname + '?bust=' + Date.now();

    } catch (e) {
        console.error("Reset failed", e);
        window.location.reload(true);
    }
}
