// src/client/client.ts
export class WebSocketClient {
    private socket: WebSocket | null = null;

    constructor(private url: string) {}

    connect() {
        this.socket = new WebSocket(this.url);
        this.socket.onopen = this.onOpen.bind(this);
        this.socket.onmessage = this.onMessage.bind(this);
        this.socket.onerror = this.onError.bind(this);
        this.socket.onclose = this.onClose.bind(this);
    }

    private onOpen() {
        console.log('WebSocket connection opened');
        this.sendMessage('Hello from the client!');
    }

    private onMessage(event: MessageEvent) {
        console.log('Message from server ', event.data);
    }

    private onError(event: Event) {
        console.error('WebSocket error: ', event);
    }

    private onClose() {
        console.log('WebSocket connection closed');
    }

    sendMessage(message: string) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(message);
        } else {
            console.log('Connection not open.');
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}