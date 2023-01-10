"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок
"""
import subprocess

from tabulate import tabulate
from task_9_1 import ip_address_updater
from task_9_2 import host_range_ping


def host_ping(addresses: list, timeout=500, requests=1):
    addresses = ip_address_updater(addresses)
    results = {"Доступные узлы": [], "Недоступные узлы": []}

    for address in addresses:
        proc = subprocess.Popen(f"ping {address} -w {timeout} -n {requests}", shell=False, stdout=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            print(f"{address} - Узел доступен")
            results["Доступные узлы"].append(str(address))
        else:
            print(f"{address} - Узел недоступен")
            results["Недоступные узлы"].append(str(address))
    return results


def host_range_ping_tab():
    res_dict = host_range_ping("192.168.0.100", 5)
    print(tabulate([res_dict], headers='keys', tablefmt="pipe", stralign="center"))


if __name__ == "__main__":
    host_range_ping_tab()
