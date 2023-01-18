"""Программа-клиент"""
import argparse
import logging
import sys
import json
import socket
import time
import threading

from Lesson_11_Vystrchil.Metaclass import ClientMaker
from Lesson_11_Vystrchil.common.logs_decorator import log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, \
    SENDER, EXIT, DESTINATION
from common.utils import get_message, send_message

logger = logging.getLogger("client")


class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()


    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    def create_message(self):
        to = input("Введите получателя сообщения: ")
        message = input("Введите сообщение для отправки: ")
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f"Сформирован словарь сообщения: {message_dict}")
        try:
            send_message(self.sock, message_dict)
            logger.info(f"Отправлено сообщение для пользователя {to}")
        except:
            logger.critical("Потеряно соединение с сервером.")
            exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input("Введите команду: ")
            if command == "message":
                self.create_message()
            elif command == "help":
                self.print_help()
            elif command == "exit":
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print("Завершение соединения.")
                logger.info("Завершение работы по команде пользователя.")
                time.sleep(1)
                break
            else:
                print("Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.")

    def print_help(self):
        print("Поддерживаемые команды:")
        print("message - отправить сообщение. Кому и текст будет запрошены отдельно.")
        print("help - вывести подсказки по командам")
        print("exit - выход из программы")


class ClientReader(threading.Thread , metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f"\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}")
                    logger.info(f"Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}")
                else:
                    logger.error(f"Получено некорректное сообщение с сервера: {message}")
            except:
                logger.critical("Потеряно соединение с сервером.")
                break


@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f"Сформировано {PRESENCE} сообщение для пользователя {account_name}")
    return out


@log
def process_response_ans(message):
    logger.debug(f"Разбор приветственного сообщения от сервера: {message}")
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        elif message[RESPONSE] == 400:
            raise ValueError(f"400 : {message[ERROR]}")
    raise ValueError(RESPONSE)

@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", default=DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument("port", default=DEFAULT_PORT, type=int, nargs="?")
    parser.add_argument("-n", "--name", default=None, nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        logger.critical(
            f"Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.")
        exit(1)

    return server_address, server_port, client_name


def main():
    print("Консольный месседжер. Клиентский модуль.")

    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input("Введите имя пользователя: ")
    else:
        print(f"Клиентский модуль запущен с именем: {client_name}")

    logger.info(
        f"Запущен клиент с парамертами: адрес сервера: {server_address}, "
        f"порт: {server_port}, имя пользователя: {client_name}")

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        logger.info(f"Установлено соединение с сервером. Ответ сервера: {answer}")
        print(f"Установлено соединение с сервером.")
    except json.JSONDecodeError:
        logger.error("Не удалось декодировать полученную Json строку.")
        exit(1)
    except:
        logger.error(f"Возникла ошибка")
        exit(1)
    else:
        module_reciver = ClientReader(client_name , transport)
        module_reciver.daemon = True
        module_reciver.start()

        module_sender = ClientSender(client_name , transport)
        module_sender.daemon = True
        module_sender.start()
        logger.debug("Запущены процессы")

        while True:
            time.sleep(1)
            if module_reciver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
