from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from settings import settings


class LedLineGpio:
    """Класс для управления линией gpio для LED"""
    
    def __init__(self, line: int, gpio_path: str, consumer: str) -> None:
        self.line = line
        self._request = request_lines(
            path=gpio_path,
            consumer=consumer,
            config={
                self.line: LineSettings(
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


class MotorDCLineGpio:
    """Класс для управления линией GPIO для DC мотора"""

    def __init__(self, line_in1: int, line_in2: int, gpio_path: str, consumer: str) -> None:
        self.line_in1 = line_in1
        self._request_in1 = request_lines(
            path=gpio_path,
            consumer=consumer,
            config={
                self.line_in1: LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=Value.INACTIVE
                )
            }
        )

        self.line_in2 = line_in2
        self._request_in2 = request_lines(
            path=gpio_path,
            consumer=consumer,
            config={
                self.line_in2: LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=Value.INACTIVE
                )
            }
        )

    def forward_motor(self) -> None:
        """Метод для вращения мотора вперёд"""

        self._request_in1.set_value(self.line_in1, Value.ACTIVE)
        self._request_in2.set_value(self.line_in2, Value.INACTIVE)

    def backward_motor(self) -> None:
        """Метод для вращения мотора назад"""

        self._request_in1.set_value(self.line_in1, Value.INACTIVE)
        self._request_in2.set_value(self.line_in2, Value.ACTIVE)

    def stop_motor(self) -> None:
        """Метод для остановки мотора"""

        self._request_in1.set_value(self.line_in1, Value.INACTIVE)
        self._request_in2.set_value(self.line_in2, Value.INACTIVE)

    def close(self) -> None:
        """Метод для освобождения ресурса"""

        self._request_in1.release()
        self._request_in2.release()


class RobotControl:
    """Класс для управления роботом"""
    
    def __init__(self) -> None:
        self._left_motor = MotorDCLineGpio(
            line_in1=settings.gpio_lines.left_motor_line_in1,
            line_in2=settings.gpio_lines.left_motor_line_in2,
            gpio_path=settings.gpio_lines.gpio_path,
            consumer=settings.gpio_lines.left_motor_consumer
        )
        
        self._right_motor = MotorDCLineGpio(
            line_in1=settings.gpio_lines.right_motor_line_in1,
            line_in2=settings.gpio_lines.right_motor_line_in2,
            gpio_path=settings.gpio_lines.gpio_path,
            consumer=settings.gpio_lines.right_motor_consumer
        )

        self.stop()

    def forward(self) -> None:
        """Движение робота вперёд"""
        
        self._left_motor.forward_motor()
        self._right_motor.forward_motor()        

    def backward(self) -> None:
        """Движение робота назад"""
        
        self._left_motor.backward_motor()
        self._right_motor.backward_motor()

    def left(self) -> None:
        """Поворот робота налево"""

        self._right_motor.forward_motor()
        self._left_motor.backward_motor()

    def right(self) -> None:
        """Поворот робота направо"""

        self._right_motor.backward_motor()
        self._left_motor.forward_motor()

    def stop(self) -> None:
        """Остановка робота"""

        self._left_motor.stop_motor()
        self._right_motor.stop_motor()

    def close(self) -> None:
        """Освобождение ресурса"""
        
        self._left_motor.close()
        self._right_motor.close()
