import unittest

import sys
import time

from Lesson_4_Vystrchil import client
from variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT


class TestClient(unittest.TestCase):

    # TESTS for client.create_presence

    def test_create_presence_time(self):
        self.assertAlmostEqual(client.create_presence()[TIME], time.time(), 2)

    def test_create_presence_default_name(self):
        self.assertEqual(client.create_presence()[USER], {ACCOUNT_NAME: "Guest"})

    def test_create_presence_real_name(self):
        self.assertEqual(client.create_presence("Mike")[USER], {ACCOUNT_NAME: "Mike"})

    def test_create_presence_action(self):
        self.assertEqual(client.create_presence()[ACTION], PRESENCE)

    def test_create_presence_type(self):
        self.assertEqual(type(client.create_presence()), type(dict({})))

    # TESTS for client.process_ans

    def test_process_ans_response_200(self):
        self.assertEqual(client.process_ans({RESPONSE: 200}), '200 : OK')

    def test_process_ans_response_400(self):
        self.assertEqual(client.process_ans({RESPONSE: 404, ERROR: "400"}), f'400 : 400')

    def test_process_ans_value_error(self):
        self.assertRaises(ValueError, client.process_ans, {})

    # TESTS for client.main

    # def test_main_value_error(self):
    #     sys.argv = sys.argv[:1] + ["192.168.1.2", "1"]
    #     print(sys.argv)
    #     self.assertRaises(ValueError, client.main)
        # try:
        #     client.main()
        # except ValueError:
        #     raise ValueError
        # except Exception:
        #     self.fail("Unexpected exception raised")
        # else:
        #     self.fail("ValueError not raised")

    # def test_main(self):
    #     sys.argv = sys.argv[:1] + ["192.168.1.2", "8000"]
    #
    #     server = SimpleServer(('127.0.0.1', 0))
    #     server.start()
    #     client = gevent.socket.create_connection(('127.0.0.1', server.server_port))
    #     response = client.makefile().read()
    #     assert response == 'hello and goodbye!'
    #     server.stop()

if __name__ == "__main__":
    unittest.main()
