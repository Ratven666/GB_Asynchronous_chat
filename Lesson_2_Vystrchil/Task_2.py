# {"orders": []}

import json


def get_all_orders(filename="orders.json"):
    with open(filename) as file:
        return json.load(file)


def write_order_to_json(item, quantity, price, buyer, date, filename="orders.json"):
    orders = get_all_orders(filename)
    order = {"item": item,
              "quantity": quantity,
              "price": price,
              "buyer": buyer,
              "date": date}
    orders["orders"].append(order)
    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=4)


if __name__ == "__main__":

    order_1 = ["staff_1", 6, 100500, "Mike", "02/12/2022"]
    order_2 = ["staff_2", 2, 1234.4567, "John", "01/12/2022"]
    write_order_to_json(*order_1)
    write_order_to_json(*order_2)

    orders = get_all_orders()
    print(orders)

