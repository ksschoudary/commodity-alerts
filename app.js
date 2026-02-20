/**
 * Emergency Reset & Cache Clear
 * Mirroring the "🚀 Emergency Reset & Refresh" from your Streamlit model
 */
async function emergencyReset() {
    const btn = document.getElementById('refresh-btn');
    btn.innerText = "Syncing...";
    btn.disabled = true;

    try {
        // 1. Clear Service Worker Caches
        if ('caches' in window) {
            const cacheNames = await caches.keys();
            await Promise.all(
                cacheNames.map(name => caches.delete(name))
            );
            console.log("Service Worker Cache Cleared");
        }

        // 2. Unregister Service Workers
        if ('serviceWorker' in navigator) {
            const registrations = await navigator.serviceWorker.getRegistrations();
            for (let registration of registrations) {
                await registration.unregister();
            }
            console.log("Service Workers Unregistered");
        }

        // 3. Force Reload bypassing browser cache
        // We add a timestamp to the URL to ensure the server treats it as a fresh request
        const freshUrl = window.location.origin + window.location.pathname + '?t=' + new Date().getTime();
        window.location.replace(freshUrl);

    } catch (error) {
        console.error("Reset Failed:", error);
        btn.innerText = "Reset Failed";
        btn.disabled = false;
    }
}
