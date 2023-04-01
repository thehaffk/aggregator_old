from redis.asyncio import Redis

from homepp.core.protocols.socket_gateway import ControllerSocketGateway


class ControllerSocketGatewayImpl(ControllerSocketGateway):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def set_connected(self, hw_key: str) -> None:
        await self._redis.set(f"controllers:{hw_key}", "connected")

    async def set_disconnected(self, hw_key: str) -> None:
        await self._redis.set(f"controllers:{hw_key}", "disconnected")

    async def is_connected(self, hw_key: str) -> bool:
        status = await self._redis.get(f"controllers:{hw_key}")
        return status == b"connected"
