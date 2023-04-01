import logging
from typing import Dict, Optional
from websockets.client import WebSocketClientProtocol

from homepp.core.protocols.socket_manager import ControllerSocketManager

Connections = Dict[str, WebSocketClientProtocol]

logger = logging.getLogger()


class ControllerSocketManagerImpl(ControllerSocketManager):
    def __init__(self, sockets: Optional[Connections] = None) -> None:
        self._sockets = sockets or {}

    async def connect(
        self, hw_key: str, websocket: WebSocketClientProtocol
    ) -> None:
        socket = websocket
        self._sockets[hw_key] = socket

    async def disconnect(self, hw_key: str) -> None:
        try:
            socket = self._sockets.pop(hw_key)
        except KeyError:
            logger.info("controller: %s already disconnect", hw_key)
        else:
            await socket.close()

    async def close(self) -> None:
        for socket in self._sockets.values():
            await socket.close()
