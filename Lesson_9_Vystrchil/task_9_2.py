"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""

from ipaddress import ip_address
from task_9_1 import host_ping


def host_range_ping(start_ip, n):
    try:
        last_octet = int(start_ip.split(".")[3])
    except (ValueError, IndexError) as e:
        raise ValueError("Некорректный тип IP адреса")

    assert isinstance(n, int), "n должно быть целым числом"
    max_n = 254 - last_octet
    if n > max_n:
        raise ValueError(f"n должен быть меньше {max_n}")
    host_list = []
    for i in range(n):
        host_list.append(str(ip_address(start_ip) + i))
    return host_ping(host_list)


if __name__ == "__main__":
    host_range_ping("192.168.0.100", 5)
