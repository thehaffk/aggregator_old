import asyncio
import logging
import logging.config

from homepp.config.settings import Settings
from homepp.presentation.ws.factory import build_server
from homepp.presentation.ws.handler import handle_accept_client

logger = logging.getLogger()


if __name__ == "__main__":
    settings = Settings()
    logging.config.fileConfig(settings.logging_config_path.strip())

    logger.info("Start aggregator")
    try:
        asyncio.run(build_server(settings, handle_accept_client))
    except KeyboardInterrupt:
        logger.info("Shuttdown aggregator")
