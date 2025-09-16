from enum import Enum


class FormResponse(Enum):
    """Класс для формирования ответа"""

    NOT_FOUND_COMMAND = (404, 'Unknown command!')
    OK_COMMAND = (200, 'Command executed')
    SERVER_ERR = (500, 'Internal Server Error!')

    @property
    def response(self) -> dict[str, int | str]:
        """Словарь для формирования ответа серверу"""

        return {
            'status': self.value[0],
            'message': self.value[1]
        }

    def get_response_err(self, name_err: str, message_err: str) -> dict[str, int | str]:
        """Метод для формирования ответа серверу с ошибкой"""
        
        return {
            'status': self.value[0],
            'name_error': name_err,
            'message': message_err
        }
