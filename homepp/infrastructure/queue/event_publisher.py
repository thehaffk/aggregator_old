import aio_pika
import logging
import json

from homepp.core.protocols.event_publisher import EventPublisher

logger = logging.getLogger()


class RabbitMQEventPublisher(EventPublisher):
    def __init__(
        self,
        connection: aio_pika.abc.AbstractRobustConnection,
        channel: aio_pika.abc.AbstractChannel,
    ):
        self._connection = connection
        self._channel = channel

    async def publish_event(self, event: dict, queue: str):
        queue_name = f"client_{queue}"
        await self._channel.declare_queue(queue_name, durable=True)
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(event).encode()),
            routing_key=queue_name,
        )
        logger.info("Event %s published to %s", event, queue_name)

    async def close(self):
        await self._connection.close()
