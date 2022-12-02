import re
import csv
from chardet import detect


data_files = ["info_1.txt", "info_2.txt", "info_3.txt"]
characteristics = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]


def get_regular_expression(characteristic: str):
    return f"({characteristic}:)\\s+(.+)"


def get_decode_string_from_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
        s = data.decode(encoding=detect(data)['encoding'])
    return s


def get_data(data_files, characteristics):
    main_data = {}

    for characteristic in characteristics:
        main_data[characteristic] = []

    for filename in data_files:
        s = get_decode_string_from_file(filename)
        for characteristic in characteristics:
            match = re.search(get_regular_expression(characteristic), s)
            main_data[characteristic].append(match[2].strip())
    return main_data


def write_to_csv(csv_file, data_files=data_files, characteristics=characteristics):
    data = get_data(data_files, characteristics)
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        headers = list(data.keys())
        writer.writerow(headers)
        for idx in range(len(data[headers[0]])):
            item = []
            for head in headers:
                item.append(data[head][idx])
            writer.writerow(item)


if __name__ == "__main__":
    write_to_csv("Result_task_1.csv")
