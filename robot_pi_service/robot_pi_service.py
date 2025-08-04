import asyncio
from websockets import serve, exceptions
from websockets.legacy.server import WebSocketServerProtocol
from json import loads, JSONDecodeError

from settings import settings
from gpio_control import LedLineGpio


async def robot_control_gpio(websocket: WebSocketServerProtocol):
    """
    Асинхронная функция для управлением gpio робота (через websocket)
    """

    try:
        led_line_gpio = LedLineGpio(line=6)
        action = None

        while True:
            try:
                command = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                data = loads(command)
            except asyncio.TimeoutError as err:
                print('Таймаут ожидания команды от клиента')
                continue  # продолжение цикла, чтобы не закрывать соединение
            except JSONDecodeError:
                print("Ошибка при декодировании JSON")
                continue
            
            match next(iter(data), None):
                case settings.commands_robot.forward:
                    if data.get(settings.commands_robot.forward):
                        action = 'Робот едет вперёд'
                        led_line_gpio.on()
                    else:
                        action = 'Команда вперёд стоп'
                        led_line_gpio.off()
                    print(action)
                    await websocket.send(message=action)
                case settings.commands_robot.backward:
                    action = 'Робот едет назад'
                    print(action)
                    await websocket.send(message=action)
                case settings.commands_robot.left:
                    action = 'Робот едет налево'
                    print(action)
                    await websocket.send(message=action)
                case settings.commands_robot.right:
                    action = 'Робот едет направо'
                    print(action)
                    await websocket.send(message=action)
    except exceptions.ConnectionClosed:
        pass
    except (exceptions.ConnectionClosedOK, exceptions.InvalidMessage, exceptions.InvalidState) as err:
        message_err = f'{err.__class__.__name__}: {err}'
        print(message_err)
        await websocket.send(message=message_err)
    except Exception as err:
        message_err = f'{err.__class__.__name__}: {err}'
        print(message_err)
        await websocket.send(message=message_err)
    finally:
        led_line_gpio.close()


async def start():
    """Асинхронная функция запуска вебсокета и бесконечного цикла"""

    print('Старт сервиса робота для приёма команд.')

    async with serve(handler=robot_control_gpio, host=settings.websocket_host, port=settings.websocket_port):
        # бесконечный цикл
        await asyncio.Future()


def run_app():
    """Функция старата приложения"""

    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Выключение сервиса робота для приёма команд.')


if __name__ == '__main__':
    run_app()
