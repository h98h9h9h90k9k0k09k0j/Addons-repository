function navigateTo(page, clientId) {
    sessionStorage.setItem('clientId', clientId);
    window.location.href = page;
}
