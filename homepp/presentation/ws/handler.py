import aiohttp
import json
import logging.config
from websockets.exceptions import ConnectionClosedError
from websockets.client import WebSocketClientProtocol

from homepp.core.protocols.socket_gateway import ControllerSocketGateway
from homepp.core.protocols.socket_manager import ControllerSocketManager
from homepp.core.protocols.event_publisher import EventPublisher

logger = logging.getLogger()


def make_error_message(detail: str) -> str:
    return json.dumps({"type": "error", "detail": detail})


# TODO: add error and event mapping
async def handle_accept_client(
    websocket: WebSocketClientProtocol,
    socket_gateway: ControllerSocketGateway,
    socket_manager: ControllerSocketManager,
    client_session: aiohttp.ClientSession,
    event_publisher: EventPublisher,
    api_url: str,
):
    hw_key = websocket.request_headers.get("HardwareKey")
    if not hw_key:
        await websocket.send(make_error_message("Hardware key not not send"))
        return

    try:
        async with client_session.get(
            f"{api_url}/controllers/client",
            params={"hw_key": hw_key},
        ) as response:
            response.raise_for_status()
            data = await response.text()
            client_id = json.loads(data)["client_id"]
            pass
    except aiohttp.ClientResponseError as e:
        logger.exception(e)
        await websocket.send(make_error_message("Hardware key not registered"))
        return

    await socket_manager.connect(hw_key, websocket)
    await socket_gateway.set_connected(hw_key)
    try:
        async for message in websocket:
            event = json.loads(message)
            await event_publisher.publish_event(event, client_id)

    except ConnectionClosedError:
        await socket_manager.disconnect(hw_key)
        await socket_gateway.set_disconnected(hw_key)
        await event_publisher.publish_event(
            {"hw_key": hw_key, "status": "disconnected"}, client_id
        )
