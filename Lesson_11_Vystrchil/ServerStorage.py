import logging
import os
from threading import Lock

from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, DateTime, ForeignKey

from Lesson_11_Vystrchil.common.variables import DATABASE_NAME

logger = logging.getLogger('server')


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ServerStorage(metaclass=SingletonMeta):
    __db_metadata = MetaData()

    def __init__(self):
        self.__path = os.path.join("data_bases", DATABASE_NAME)
        self.__engine = create_engine(f'sqlite:///{self.__path}')
        self.clients_db_table = self.__create_clients_table()
        self.client_history_db_table = self.__create_client_history_table()
        self.contact_list_db_table = self.__create_contact_list_table()
        self.init_db()

    def init_db(self):
        db_is_created = os.path.exists(self.__path)
        if not db_is_created:
            self.__db_metadata.create_all(self.__engine)
        else:
            logger.info("Такая БД уже есть!")

    def __create_clients_table(self):
        clients_db_table = Table("clients", self.__db_metadata,
                                 Column("id", Integer, primary_key=True),
                                 Column("login", String(50), nullable=False),
                                 Column("info", String(200))
                                 )
        return clients_db_table

    def __create_client_history_table(self):
        client_history_db_table = Table("client_history", self.__db_metadata,
                                        Column("id", Integer, primary_key=True),
                                        Column("entry_time", DateTime(timezone=True), nullable=False),
                                        Column("info", String(200)),
                                        Column("client_id", Integer, ForeignKey("clients.id"))
                                        )
        return client_history_db_table

    def __create_contact_list_table(self):
        contact_list_db_table = Table("contact_list", self.__db_metadata,
                                      Column("owner_id", Integer, ForeignKey("clients.id"), primary_key=True),
                                      Column("client_id", Integer, ForeignKey("clients.id"), primary_key=True)
                                      )
        return contact_list_db_table

    @property
    def engine(self):
        return self.__engine


if __name__ == "__main__":
    server_storage = ServerStorage()
