/**
 * Commodity Tracker: Master app.js
 * Handles three independent segments: Wheat News, PIB, and Regulatory
 */

// 1. Data Source Mapping
const DATA_SOURCES = {
    wheat: 'wheat_news.json',
    pib: 'pib_data.json',
    reg: 'fssai_data.json'
};

// 2. Initialize App on Page Load
document.addEventListener('DOMContentLoaded', () => {
    // Start with Wheat News by default
    switchSegment('wheat');
});

/**
 * Core function to switch segments and fetch data
 * @param {string} segment - The key from DATA_SOURCES
 */
async function switchSegment(segment) {
    const container = document.getElementById('main-feed');
    console.log("Switching to segment:", segment);

    // Update UI Button States
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.querySelector(`[data-segment="${segment}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    // Show Loading State
    container.innerHTML = `<div style="padding:40px; text-align:center; color:#8b949e;">
        <div class="spinner"></div>
        <p>Fetching latest ${segment} updates...</p>
    </div>`;

    try {
        // Fetch the specific JSON file
        const response = await fetch(DATA_SOURCES[segment]);
        
        // Handle 404 or file not found errors
        if (!response.ok) {
            throw new Error(`File ${DATA_SOURCES[segment]} not found.`);
        }

        const data = await response.json();
        console.log(`Data received for ${segment}:`, data);

        // Handle empty datasets
        if (!data || data.length === 0) {
            container.innerHTML = `
                <div style="padding:40px; text-align:center; color:#8b949e;">
                    <p>No recent ${segment} updates found.</p>
                    <p style="font-size:0.8rem;">(Check if the GitHub Scraper ran correctly)</p>
                </div>`;
            return;
        }

        // Render the news cards
        renderFeed(data, segment);

    } catch (error) {
        console.error("Fetch Error:", error);
        container.innerHTML = `
            <div style="padding:40px; text-align:center; color:#e74c3c;">
                <p><strong>Error Loading Data</strong></p>
                <p style="font-size:0.8rem; color:#8b949e;">${error.message}</p>
            </div>`;
    }
}

/**
 * Creates HTML cards from JSON data
 * @param {Array} data - The array of news items
 * @param {string} type - The current segment type for styling
 */
function renderFeed(data, type) {
    const container = document.getElementById('main-feed');
    
    const html = data.map(item => {
        // Setup Segment-Specific Labels
        let badgeText = item.date || 'New';
        let sourceLabel = 'Market Feed';

        if (type === 'pib') {
            badgeText = item.aging || 'Fresh';
            sourceLabel = 'PIB Govt of India';
        } else if (type === 'reg') {
            sourceLabel = 'FSSAI Regulatory';
        }

        // Return the HTML card structure
        return `
            <div class="card" data-type="${type}">
                <div class="card-header">
                    <span class="badge">${badgeText}</span>
                    <span class="source-label">${sourceLabel}</span>
                </div>
                <h3 class="card-title">${item.title}</h3>
                <div class="card-footer">
                    <a href="${item.url}" target="_blank" class="view-btn">
                        Read Full Release →
                    </a>
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}
