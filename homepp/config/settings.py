import os
from dataclasses import dataclass, field


@dataclass(slots=True)
class RabbitMQSettings:
    username: str = field(init=False)
    password: str = field(init=False)
    host: str = field(init=False)
    port: int = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.username = os.getenv("RABBIT_USERNAME")
        self.password = os.getenv("RABBIT_PASSWORD")
        self.host = os.getenv("RABBIT_HOST")
        self.port = os.getenv("RABBIT_PORT")
        self.url = "amqp://{username}:{password}@{host}:{port}/".format(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )


@dataclass(slots=True)
class RedisSettings:
    host: str = field(init=False)
    port: int = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")


@dataclass
class ServerSettings:
    host: str = field(init=False)
    port: int = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.host = os.getenv("SERVER_HOST")
        self.port = os.getenv("SERVER_PORT")


@dataclass(slots=True)
class Settings:
    server: ServerSettings = field(init=False, default_factory=ServerSettings)
    redis: RedisSettings = field(init=False, default_factory=RedisSettings)
    rabbit: RabbitMQSettings = field(
        init=False, default_factory=RabbitMQSettings
    )
    logging_config_path: str = field(init=False)
    api_url: str = field(init=False)

    def __post_init__(self):
        self._read_env()

    def _read_env(self):
        self.logging_config_path = os.getenv("LOGGING_CONFIG_PATH")
        self.api_url = os.getenv("API_URL")
