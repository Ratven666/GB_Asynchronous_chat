"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

if __name__ == "__main__":

    words = "attribute", "класс", "функция", "type"
    latin_liter_words = []
    rus_liter_words = []

    for word in words:
        try:
            latin_liter_words.append(bytes(word, "ascii"))
        except UnicodeEncodeError:
            rus_liter_words.append(word)

    print(f"Слова которые можно записать с помощью маркировки b'': {latin_liter_words}")
    print(f"Слова которые нельзя записать с помощью маркировки b'': {rus_liter_words}")
