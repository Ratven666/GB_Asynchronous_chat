"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""


import subprocess
import chardet

yandex = subprocess.Popen(['ping', 'yandex.ru'], stdout=subprocess.PIPE)
youtube = subprocess.Popen(['ping', 'youtube.ru'], stdout=subprocess.PIPE)

sites = yandex, youtube

i = 0
while(True):
    for line in sites[i % 2].stdout:
        result = chardet.detect(line)
        print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
        break
    i += 1
    print("*" * 100)
