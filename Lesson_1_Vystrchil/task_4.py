"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

if __name__ == "__main__":

    words = "разработка", "администрирование", "protocol", "standard"

    for word in words:
        word = word.encode(encoding="UTF-8")
        print(word)
        word = word.decode(encoding="UTF-8")
        print(word, "\n")
