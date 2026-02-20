// Configuration for the 28 Commodities
const commodityList = ["Wheat", "Sugar", "Palm Oil", "Chana", "Soyabean", "Turmeric", "Cashew", "Isabgol", "Maize", "Paddy", "Groundnut", "Sunflower oil", "Cotton seed oil", "Almond", "Black pepper", "Cardamom", "Chilli powder", "Ethanol", "Potato", "Milk", "Dairy", "Cocoa", "Oats", "Raisins", "Cabbage", "Carrot", "Ring beans", "Onion"];

async function refreshAllUpdates() {
    // These run independently
    loadWheatNews();
    loadPIBUpdates();
    loadRegulatoryUpdates();
}

// 1. Wheat News: Max 100 items or 6 months aging
async function loadWheatNews() {
    const res = await fetch('wheat_news.json');
    let data = await res.json();
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

    const filtered = data
        .filter(item => new Date(item.date) >= sixMonthsAgo)
        .slice(0, 100);
        
    renderFeed('wheat', filtered);
}

// 2. PIB Updates: Freshness based, no time limit, max 100
async function loadPIBUpdates() {
    const res = await fetch('pib_data.json');
    let data = await res.json();
    
    // Sort by freshness and take top 100
    const filtered = data.slice(0, 100);
    renderFeed('pib', filtered);
}

// 3. Regulatory: FSSAI & Framework News
async function loadRegulatoryUpdates() {
    const res = await fetch('fssai_data.json');
    let data = await res.json();
    renderFeed('reg', data);
}

window.onload = refreshAllUpdates;
