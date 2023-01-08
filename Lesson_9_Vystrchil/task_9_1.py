"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""

from ipaddress import ip_address
import subprocess


def ip_address_updater(addresses: list):
    updated_list = []
    for ip in addresses:
        try:
            updated_list.append(ip_address(ip))
        except ValueError:
            updated_list.append(ip)
    return updated_list


def host_ping(addresses: list, timeout=500, requests=1):
    addresses = ip_address_updater(addresses)

    for address in addresses:
        proc = subprocess.Popen(f"ping {address} -w {timeout} -n {requests}", shell=False, stdout=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            print(f"{address} - Узел доступен")
        else:
            print(f"{address} - Узел недоступен")


if __name__ == "__main__":
    ip_addresses = ["yandex.ru", "rutracker.org", "2.2.2.2", "192.168.0.100", "192.168.0.101", "127.0.0.1"]

    host_ping(ip_addresses)
