"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

if __name__ == "__main__":

    word_list = [b"class", b"function", b"method"]

    for word in word_list:
        print(type(word), word, len(word), sep="\t")
