// src/client/connection.ts
import { WebSocketClient } from "./client";

const serverUrl = 'ws://localhost:3030'; // Change this URL to your WebSocket server URL
export const wsClient = new WebSocketClient(serverUrl);