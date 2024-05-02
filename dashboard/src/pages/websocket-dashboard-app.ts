// src/pages/matter-dashboard-app.ts
import { wsClient } from '../client/connection';

class MatterDashboardApp extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <h1>WebSocket Dashboard</h1>
            <button id="connect">Connect</button>
            <button id="send">Send Message</button>
            <button id="disconnect">Disconnect</button>
        `;

        this.querySelector('#connect')!.addEventListener('click', () => {
            wsClient.connect();
        });

        this.querySelector('#send')!.addEventListener('click', () => {
            wsClient.sendMessage('Hello, WebSocket Server!');
        });

        this.querySelector('#disconnect')!.addEventListener('click', () => {
            wsClient.disconnect();
        });
    }
}

customElements.define('matter-dashboard-app', MatterDashboardApp);