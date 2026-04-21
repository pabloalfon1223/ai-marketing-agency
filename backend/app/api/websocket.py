from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Any
import json

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    """Manages active WebSocket connections for real-time updates."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict[str, Any]):
        """Broadcast a message to all connected clients."""
        data = json.dumps(message)
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(data)
            except Exception:
                disconnected.append(connection)
        # Clean up dead connections
        for conn in disconnected:
            self.active_connections.remove(conn)

    async def broadcast_task_update(self, task_id: int, status: str, agent_type: str):
        """Convenience method for broadcasting task status changes."""
        await self.broadcast({
            "type": "task_update",
            "task_id": task_id,
            "status": status,
            "agent_type": agent_type,
        })

    async def broadcast_content_update(self, content_id: int, status: str):
        """Convenience method for broadcasting content status changes."""
        await self.broadcast({
            "type": "content_update",
            "content_id": content_id,
            "status": status,
        })

    async def broadcast_log(self, task_id: int, agent_type: str, message: str):
        """Convenience method for broadcasting agent log messages."""
        await self.broadcast({
            "type": "agent_log",
            "task_id": task_id,
            "agent_type": agent_type,
            "message": message,
        })


# Singleton instance - import this from other modules
manager = ConnectionManager()


@router.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive by waiting for messages
            # Clients can send ping/pong or commands
            data = await websocket.receive_text()
            # Echo back as acknowledgment
            await websocket.send_text(json.dumps({"type": "ack", "data": data}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
