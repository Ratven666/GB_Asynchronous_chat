import socket
import time
import json
import sys


def create_presence(account_name="Mike"):
    out = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": account_name
        }
    }
    return out


def process_ans(message):
    if "response" in message:
        if message["response"] == 200:
            return "200 : OK"
        return f"400 : {message['error']}"
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError("В качестве порта может быть указано только число в диапазоне от 1024 до 65535.")
    except IndexError:
        server_address = "127.0.0.1"
        server_port = 7777
    except ValueError:
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()

    js_message = json.dumps(message_to_server)
    encoded_message = js_message.encode("utf-8")
    transport.send(encoded_message)

    try:
        encoded_response = transport.recv(1024)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode("utf-8")
            response = json.loads(json_response)
            if isinstance(response, dict):
                answer = process_ans(response)
                print(answer)
            raise ValueError
        raise ValueError
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
