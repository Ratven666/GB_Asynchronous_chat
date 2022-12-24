"""Программа-клиент"""
import argparse
import logging
import sys
import json
import socket
import time

from Lesson_7_Vystrchil.common.logs_decorator import log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, \
    SENDER
from common.utils import get_message, send_message

logger = logging.getLogger("client")


@log
def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.info(f"Для пользователя {account_name} пдготовленно сообщение типа {PRESENCE}")
    return out

@log
def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    logger.info(f"Сообщение от сервера: {message}")
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f"Получено сообщение от пользователя "
              f"{message[SENDER]}:\n{message[MESSAGE_TEXT]}")
        logger.info(f"Получено сообщение от пользователя "
                    f"{message[SENDER]}:\n{message[MESSAGE_TEXT]}")
    else:
        logger.error(f"Получено некорректное сообщение с сервера: {message}")


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input("Введите сообщение для отправки или \'!!!\' для завершения работы: ")
    if message == "!!!":
        sock.close()
        logger.info("Завершение работы по команде пользователя.")
        print("Спасибо за использование нашего сервиса!")
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    logger.debug(f"Сформирован словарь сообщения: {message_dict}")
    return message_dict


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", default=DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs="?")
    parser.add_argument("-m", "--mode", default="listen", nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(f"Попытка запуска клиента с неподходящим номером порта: {server_port}.")
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ("listen", "send"):
        logger.critical(f"Указан недопустимый режим работы {client_mode}, "
                        f"допустимые режимы: listen , send")
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    '''
    Загружаем параметы коммандной строки
    :return:
    '''
    server_address, server_port, client_mode = arg_parser()

    logger.info(
        f"Запущен клиент с парамертами: адрес сервера: {server_address}, "
        f"порт: {server_port}, режим работы: {client_mode}")

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_ans(get_message(transport))
        logger.info(f"Установлено соединение с сервером. Ответ сервера: {answer}")
        print("Установлено соединение с сервером.")
    except json.JSONDecodeError:
        logger.error("Не удалось декодировать полученную Json строку.")
        sys.exit(1)
    except ConnectionRefusedError:
        logger.critical(
            f"Не удалось подключиться к серверу {server_address}:{server_port}, "
            f"конечный компьютер отверг запрос на подключение.")
        sys.exit(1)
    except Exception:
        logger.error("Что-то сработало не так(")
        sys.exit(1)
    else:

        # основной цикл прогрммы:
        if client_mode == "send":
            print("Режим работы - отправка сообщений.")
        if client_mode == "listen":
            print("Режим работы - приём сообщений.")
        while True:
            # режим работы - отправка сообщений
            if client_mode == "send":
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f"Соединение с сервером {server_address} было потеряно.")
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == "listen":
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f"Соединение с сервером {server_address} было потеряно.")
                    sys.exit(1)


if __name__ == '__main__':
    main()
