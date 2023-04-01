import aiohttp
import asyncio
import aio_pika
import logging.config
from functools import partial
from redis.asyncio import Redis
from websockets.server import serve

from homepp.config.settings import Settings
from homepp.infrastructure.queue.event_publisher import RabbitMQEventPublisher
from homepp.infrastructure.sockets.socket_gateway import (
    ControllerSocketGatewayImpl,
)
from homepp.infrastructure.sockets.socket_manager import (
    ControllerSocketManagerImpl,
)
from .types import Handler

logger = logging.getLogger()


async def build_server(settings: Settings, handler: Handler):
    redis = Redis(host=settings.redis.host, port=settings.redis.port)  # type: ignore # noqa
    connection = await aio_pika.connect_robust(settings.rabbit.url)
    rabbit_channel = await connection.channel()
    client_session = aiohttp.ClientSession()

    socket_gateway = ControllerSocketGatewayImpl(redis)
    socket_manager = ControllerSocketManagerImpl()
    event_publisher = RabbitMQEventPublisher(connection, rabbit_channel)

    # TODO: fix lifecycle, remove singletones
    accept_handler = partial(
        handler,
        socket_gateway=socket_gateway,
        socket_manager=socket_manager,
        event_publisher=event_publisher,
        client_session=client_session,
        api_url=settings.api_url,
    )
    return await run_server(
        accept_handler, settings.server.host, settings.server.port
    )


async def run_server(accept_handler: Handler, host: str, port: int) -> None:
    async with serve(accept_handler, host, port):
        await asyncio.Future()
