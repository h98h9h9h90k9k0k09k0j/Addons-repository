function navigateTo(page, clientId) {
    console.log(`Navigating to ${page} with client ID: ${clientId}`);
    sessionStorage.setItem('clientId', clientId);
    window.location.href = page;
}
