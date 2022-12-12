import time
import unittest

import socket
import sys
import json

from Lesson_4_Vystrchil import server
from variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from utils import get_message, send_message



class TestServer(unittest.TestCase):

    def test_process_client_message_200(self):
        self.assertEqual(server.process_client_message({ACTION: PRESENCE,
                                                        TIME: time.time(),
                                                        USER: {ACCOUNT_NAME: "Guest"}
                                                        }), {RESPONSE: 200})

    def test_process_client_message_sd(self):
        self.assertEqual(server.process_client_message({ACTION: PRESENCE,
                                                        TIME: time.time(),
                                                        USER: {ACCOUNT_NAME: "Mike"}
                                                        }), {RESPONSE: 400, ERROR: "Bad Request"})


if __name__ == "__main__":
    unittest.main()
