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
    stop: str

    def is_command(self, command: str) -> bool:
        """Есть ли команда в командах"""

        return command in self.model_dump().values()


class GpioLines(ModelConfig):
    """Класс для линий GPIO"""

    gpio_path: str
    led_line: int
    led_consumer: str
    left_motor_line_in1: int
    left_motor_line_in2: int
    left_motor_consumer: str
    right_motor_line_in1: int
    right_motor_line_in2: int
    right_motor_consumer: str


class CommandsLinux(ModelConfig):
    """Класс с командами для линукса"""

    videostream: str
    on_videostream: bool
    on_stream_debug: bool


class Settings(ModelConfig):
    """Класс для данных конфига"""

    websocket_host: str
    websocket_port: int
    commands_robot: CommandsRobot = CommandsRobot()
    commands_linux: CommandsLinux = CommandsLinux()
    gpio_lines: GpioLines = GpioLines()


settings = Settings()
