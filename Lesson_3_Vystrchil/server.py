import socket
import json
import sys


def process_client_message(message):
    if message.get("action") == "presence" and "time" in message and "user" in message:
        return {"response": 200,
                "alert": "OK"}
    return {
        "response": 400,
        "error": "Bad Request"
    }


def main():
    try:
        if "-p" in sys.argv:
            listen_port = int(sys.argv[sys.argv.index("-p") + 1])
            if listen_port < 1024 or listen_port > 65535:
                raise ValueError("Неверный номер порта!")
        else:
            listen_port = 7777
    except IndexError:
        print("После параметра -'p' необходимо указать номер порта.")
        sys.exit(1)
    except ValueError:
        sys.exit(1)

    try:
        if "-a" in sys.argv:
            listen_address = sys.argv[sys.argv.index("-a") + 1]
        else:
            listen_address = "127.0.0.1"
    except IndexError:
        print(
            "После параметра 'a'- необходимо указать адрес, который будет слушать сервер.")
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(5)

    while True:
        client, client_address = transport.accept()
        try:
            encoded_response = client.recv(1024)
            if isinstance(encoded_response, bytes):
                json_response = encoded_response.decode("utf-8")
                response = json.loads(json_response)
                if isinstance(response, dict):
                    message_from_client = response
                    print(message_from_client)
                raise ValueError
            raise ValueError

            response = process_client_message(message_from_client)
            js_message = json.dumps(response)
            encoded_message = js_message.encode("utf-8")
            client.send(encoded_message)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
