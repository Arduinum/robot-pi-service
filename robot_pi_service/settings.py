from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    """Модель конфига"""
    
    model_config = SettingsConfigDict(
        env_file = '.env', 
        env_file_encoding='utf-8',
        extra='ignore'
    )


class CommandsRobot(ModelConfig):
    """Класс с командами для робота"""

    forward: str
    backward: str
    left: str
    right: str


class Settings(ModelConfig):
    """Класс для данных конфига"""

    websocket_host: str
    websocket_port: int
    commands_robot: CommandsRobot = CommandsRobot()


settings = Settings()
