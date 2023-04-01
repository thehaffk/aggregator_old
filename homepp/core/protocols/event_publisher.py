from typing import Protocol


class EventPublisher(Protocol):
    async def publish_event(self, event: dict, queue: str) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError
