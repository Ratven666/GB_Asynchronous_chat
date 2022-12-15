import logging

from Lesson_5_Vystrchil.common.variables import LOGGING_LEVEL

client_logger = logging.getLogger("client")
formatter = logging.Formatter("%(asctime)s %(levelname)-10s %(module)s %(message)s")

file_handler = logging.FileHandler("client_log.log", encoding="utf8")
file_handler.setFormatter(formatter)

client_logger.addHandler(file_handler)
client_logger.setLevel(LOGGING_LEVEL)

if __name__ == "__main__":
    client_logger.critical("Критическая ошибка")
    client_logger.error("Ошибка")
    client_logger.debug("Отладочная информация")
    client_logger.info("Информационное сообщение")

