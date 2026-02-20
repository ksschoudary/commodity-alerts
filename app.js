// --- Configuration ---
const DATA_SOURCES = {
    wheat: 'wheat_news.json',
    pib: 'pib_data.json',
    reg: 'fssai_data.json'
};

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    // Default to 'wheat' news on first load
    switchSegment('wheat');
});

/**
 * Main function to switch between segments
 * @param {string} segment - 'wheat', 'pib', or 'reg'
 */
async function switchSegment(segment) {
    const container = document.getElementById('main-feed');
    
    // 1. Update UI Buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    // Ensure you have data-segment="wheat" etc on your HTML buttons
    const activeBtn = document.querySelector(`[data-segment="${segment}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    // 2. Show Loading State
    container.innerHTML = `<div class="loading">Fetching latest ${segment} updates...</div>`;

    // 3. Fetch and Render Data
    try {
        const response = await fetch(DATA_SOURCES[segment]);
        if (!response.ok) throw new Error('Data not found');
        
        const data = await response.json();
        
        if (data.length === 0) {
            container.innerHTML = `<div class="empty">No updates found in this category.</div>`;
            return;
        }

        renderFeed(data, segment);
    } catch (error) {
        console.error(error);
        container.innerHTML = `<div class="error">Error loading data. Ensure the scraper has run.</div>`;
    }
}

/**
 * Renders the JSON data into HTML cards
 */
function renderFeed(data, type) {
    const container = document.getElementById('main-feed');
    
    const html = data.map(item => {
        // Handle different labels for different segments
        const badgeText = type === 'pib' ? (item.aging || 'Official') : (item.date || 'Update');
        const sourceLabel = type === 'wheat' ? 'Market News' : (type === 'pib' ? 'PIB India' : 'Regulatory');

        return `
            <div class="card">
                <div class="card-header">
                    <span class="badge">${badgeText}</span>
                    <span class="source-label">${sourceLabel}</span>
                </div>
                <h3 class="card-title">${item.title}</h3>
                <div class="card-footer">
                    <a href="${item.url}" target="_blank" class="view-btn">Read Full Report</a>
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}
