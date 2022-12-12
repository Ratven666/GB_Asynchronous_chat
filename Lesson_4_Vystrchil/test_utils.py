import json
import unittest

import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from Lesson_4_Vystrchil import client, utils
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, ENCODING


class TestUtils(unittest.TestCase):

    def test_get_message(self):
        SERV_SOCK = socket(AF_INET, SOCK_STREAM)
        SERV_SOCK.bind(('', 8889))
        SERV_SOCK.listen(1)

        CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
        CLIENT_SOCK.connect(('localhost', 8889))
        CLIENT_SOCK, ADDR = SERV_SOCK.accept()
        msg = {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        utils.send_message(SERV_SOCK, msg)
        answer = utils.get_message(CLIENT_SOCK)

        CLIENT_SOCK.close()
        SERV_SOCK.close()
        self.assertEqual(msg, answer)


if __name__ == "__main__":
    unittest.main()
