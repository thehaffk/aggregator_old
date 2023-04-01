from typing import Protocol, Any


class ControllerSocketManager(Protocol):
    async def connect(self, hw_key: str, websocket: Any) -> None:
        raise NotImplementedError

    async def disconnect(self, hw_key: str) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError
