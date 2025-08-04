from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value


class LedLineGpio:
    """Класс для управления динией gpio для LED"""
    
    def __init__(self, line: int) -> None:
        self.line = line
        self._request = request_lines(
            '/dev/gpiochip0',
            consumer='led-blinker',
            config={
                line: LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=Value.INACTIVE
                )
            }
        )

    def on(self) -> None:
        """Метод для включения LED"""
        
        self._request.set_value(self.line, Value.ACTIVE)

    def off(self) -> None:
        """Метод для выключения LED"""
        
        self._request.set_value(self.line, Value.INACTIVE)

    def close(self) -> None:
        """Метод для освобождения ресурса"""
        
        self._request.release()
