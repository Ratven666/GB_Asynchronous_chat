"""Программа-сервер"""
import logging
import select
import socket
import sys
import json
import time

from Lesson_7_Vystrchil.common.logs_decorator import log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message

logger = logging.getLogger('server')


@log
def process_client_message(message, client, messages_list):
    '''
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, возвращает словарь-ответ для клиента
    :param message:
    :return:
    '''
    logger.info(f"Сообщение от клиента: {message}")
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    if ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    send_message(client, {
        RESPONSE: 400,
        ERROR: "Bad Request"
    })


@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        logger.critical("После параметра -\'p\' не указан номер порта.")
        sys.exit(1)
    except ValueError:
        logger.critical("В качастве порта заданно некорректное значение")
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except IndexError:
        logger.critical("После параметра -\'a\' не указан IP адрес.")
        sys.exit(1)

    return listen_address, listen_port


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    :return:
    '''
    listen_address, listen_port = arg_parser()

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.2)

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        # проверяем новых клиентов на подключение
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            logger.info(f"Установлено соедение - {client_address}")
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # прием сообщений
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    logger.info(f"Клиент {client_with_message.getpeername()} "
                                f"отключился от сервера.")
                    clients.remove(client_with_message)

        # отправляем сообщения
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    logger.info(f"Клиент {waiting_client.getpeername()} отключился от сервера.")
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
