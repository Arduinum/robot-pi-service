import asyncio
from functools import partial
from gpiod import exception
from subprocess import Popen, DEVNULL
from os import setpgrp, killpg, getpgid
from signal import SIGTERM
from socket import gethostbyname
from websockets import serve, exceptions
from websockets.legacy.server import WebSocketServerProtocol
from json import loads, dumps, JSONDecodeError
from time import sleep

from settings import settings
from gpio_control import RobotControl
from response_data import FormResponse


async def robot_control_gpio(
    websocket: WebSocketServerProtocol,
    robot_control: RobotControl,
    commands_status: FormResponse
) -> None:
    """
    Асинхронная функция для управлением gpio робота (через websocket)
    """

    try:
        while True:
            try:
                command = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                data = loads(command)
                command_name = data.get('command')

                if command_name != settings.commands_robot.stop:
                    robot_control.blinking_off()
                    robot_control.connected()
            except asyncio.TimeoutError as err:
                print('Таймаут ожидания команды от клиента')
                continue  # продолжение цикла, чтобы не закрывать соединение
            except JSONDecodeError:
                print('Ошибка при декодировании JSON!')
                continue

            match command_name:
                case settings.commands_robot.forward:
                    robot_control.forward()
                case settings.commands_robot.backward:
                    robot_control.backward()
                case settings.commands_robot.left:
                    robot_control.left()
                case settings.commands_robot.right:
                    robot_control.right()
                case settings.commands_robot.stop:
                    robot_control.stop()
                    robot_control.ready_to_connect()
                case _:
                    data.update(commands_status.NOT_FOUND_COMMAND.response)
                    await websocket.send(message=dumps(data))

            if settings.commands_robot.is_command(command=command_name):
                data.update(commands_status.OK_COMMAND.response)
                await websocket.send(message=dumps(data))
    except (exceptions.ConnectionClosed, exception.RequestReleasedError):
        return
    except (exceptions.ConnectionClosedOK, exceptions.InvalidMessage, exceptions.InvalidState, OSError) as err:
        message_err = f'{err.__class__.__name__}: {err}'
        print(message_err)
        data.update(
            commands_status.SERVER_ERR.get_response_err(
                name_err=err.__class__.__name__, 
                message_err=err
            )
        )
        await websocket.send(message=dumps(data))


async def start() -> None:
    """Асинхронная функция запуска вебсокета и бесконечного цикла"""

    print('Старт сервиса робота для приёма команд.')

    try:
        robot_control: RobotControl = RobotControl()
        commands_status: FormResponse = FormResponse
        
        async with serve(
            handler=partial(robot_control_gpio, robot_control=robot_control, commands_status=commands_status), 
            host=gethostbyname(settings.websocket_host), 
            port=settings.websocket_port
        ):
            # бесконечный цикл
            await asyncio.Future()
    except (asyncio.CancelledError, OSError, exception.RequestReleasedError) as err:
        # пробрасываем ошибку, чтобы asyncio.run() всё корректно закрыл
        message_err = f'{err.__class__.__name__}: {err}'
        print(message_err)
        raise
    finally:
        if robot_control is not None:
            robot_control.blinking_off()
            robot_control.close()


def run_app() -> None:
    """Функция старата приложения"""

    command_stream = None

    try:
        if settings.commands_linux.on_videostream:
            command_stream = Popen(
                settings.commands_linux.videostream, 
                shell=True, 
                preexec_fn=setpgrp, 
                stderr=None if settings.commands_linux.on_stream_debug else DEVNULL
            )
            sleep(0.1)
            print('Видеострим запущен.')
        
        asyncio.run(start())
    except KeyboardInterrupt:
        try:
            if settings.commands_linux.on_videostream and command_stream:
                killpg(getpgid(command_stream.pid), SIGTERM)
        except ProcessLookupError:
            # Если процесс был уже завершён
            pass
        finally:
            print('Выключение сервиса робота для приёма команд.')


if __name__ == '__main__':
    run_app()
