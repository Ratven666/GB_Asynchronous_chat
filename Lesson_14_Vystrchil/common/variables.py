"""Константы"""
import logging


# Порт поумолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PUBLIC_KEY = 'pubkey'
DATA = 'bin'
SENDER = 'from'
DESTINATION = 'to'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'

LOGGING_LEVEL = logging.DEBUG

MESSAGE = "message"
MESSAGE_TEXT = "mess_text"
LIST_INFO = 'data_list'
EXIT = "exit"

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {
            RESPONSE: 400,
            ERROR: None
        }
RESPONSE_205 = {
    RESPONSE: 205
}
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
RESPONSE_202 = {
    RESPONSE: 202,
    LIST_INFO: None
}

DATABASE_NAME = "Server_db.sqlite"

GET_CONTACTS = "get_contacts"
LIST_INFO = "data_list"
REMOVE_CONTACT = "remove"
ADD_CONTACT = "add"
USERS_REQUEST = "get_users"

PUBLIC_KEY_REQUEST = 'pubkey_need'
