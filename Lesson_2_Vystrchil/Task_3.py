# Задание на закрепление знаний по модулю yaml.
#
# Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
#
# Для этого:
#     Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
#     второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое
#     число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
#
#     Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
#     При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
#     а также установить возможность работы с юникодом: allow_unicode = True;
#
#     Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

import yaml


def dump_data(data, file="file.yaml"):
    with open(file, "w") as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def load_data(file="file.yaml"):
    with open(file) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


if __name__ == "__main__":

    test_data = {"list": [1, 2, 3, 4],
                 "int_numb": 42,
                 "inner_dict": {"☭": 12,
                                "\u2692": [1, 2],
                                "\u2693": "spam"}
                 }

    dump_data(test_data)

    data = load_data()
    print(data)
    print(data == test_data)
