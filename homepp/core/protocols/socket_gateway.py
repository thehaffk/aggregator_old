from typing import Protocol


class ControllerSocketGateway(Protocol):
    async def set_connected(self, hw_key: str) -> None:
        raise NotImplementedError

    async def set_disconnected(self, hw_key: str) -> None:
        raise NotImplementedError

    async def is_connected(self, hw_key: str) -> bool:
        raise NotImplementedError
