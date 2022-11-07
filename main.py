import json
import os
from typing_extensions import Self
from unicodedata import name


class Car():
    def __init__(self, name="", type=0, creator=0, money=0, color=0, privod=0, box_type=0, v_engine=0):
        self.name = str(name)
        self.type = type
        self.creator = creator
        self.color = color
        self.money = money
        self.privod = privod
        self.box_type = box_type
        self.door_status = ["открыта", "открыта", "открыта", "открыта"]
        self.rotators_status = ["не работает", "не работает"]
        self.v_engine = v_engine
        if name != "":
            self.save()
            cars_dict[str(name)] = self

    def get_info(self):
        return [f"""Имя: {self.name}
Тип машины {self.type}
Стоимость: {self.money}
Производитель: {self.creator}
Привод: {self.privod}
Тип коробки: {self.box_type}
Объем двигателя: {float(self.v_engine)}
Статус дверей:
    Правая передняя: {self.door_status[1]}
    Левая передняя: {self.door_status[0]}
    Правая задняя: {self.door_status[3]}
    Левая задняя: {self.door_status[2]}
Статус поворотников:
    Левый: {self.rotators_status[0]}
    Правый: {self.rotators_status[1]}
""", f"<font color='{self.color}' size = 21 >▉</font>"]

    def open_door(self, door_index: int):
        if self.door_status[door_index] == "открыта":
            self.door_status[door_index] = "закрыта"
        else:
            self.door_status[door_index] = "открыта"
        self.save()

    def activate_rotator(self, rotator_index: int):
        if self.rotators_status[rotator_index] == "работает":
            self.rotators_status[rotator_index] = "не работает"
        else:
            self.rotators_status[rotator_index] = "работает"
        self.save()

    def restore(self, name):
        with open(f"data/cars/{name}.json", "r") as r_file:
            car = json.load(r_file)
            self.name = car["name"]
            self.type = car["type"]
            self.creator = car["creator"]
            self.money = car["money"]
            self.color = car["color"]
            self.privod = car["privod"]
            self.box_type = car["box_type"]
            self.door_status = car["door_status"]
            self.rotators_status = car["rotators_status"]
            self.v_engine = car["v_engine"]
            cars_dict[str(self.name)] = self

    def save(self):
        with open(f"data/cars/{self.name}.json", "w", encoding="utf-8") as w_file:
            car = {
                "name": self.name,
                "type": self.type,
                "creator": self.creator,
                "color": self.color,
                "money": self.money,
                "privod": self.privod,
                "box_type": self.box_type,
                "door_status": self.door_status,
                "rotators_status": self.rotators_status,
                "v_engine": self.v_engine
            }
            json.dump(car, w_file)
        with open(f"data/info/names.json", "r", encoding="utf-8") as r_file:
            old_data = json.load(r_file)
            if self.name not in old_data["names"]:
                old_data["names"].append(self.name)
                with open(f"data/info/names.json", "w", encoding="utf-8") as r_file:
                    json.dump(old_data, r_file)

    def delete_data(self):
        os.remove(f'data/cars/{self.name}.json')
        if self.name in cars_dict.keys():
            del cars_dict[str(self.name)]
        with open(f"data/info/names.json", "r", encoding="utf-8") as r_file:
            old_data = json.load(r_file)
            if self.name in old_data["names"]:
                old_data["names"].remove(str(self.name))
            with open(f"data/info/names.json", "w", encoding="utf-8") as r_file:
                json.dump(old_data, r_file)


class Tools():
    def get_cars_list():
        with open(f"data/info/names.json", "r", encoding="utf-8") as r_file:
            names = json.load(r_file)["names"]
        return names

    def check_name(name):
        with open(f"data/info/names.json", "r", encoding="utf-8") as r_file:
            names = json.load(r_file)["names"]
            if name in names:
                return False
            else:
                return True

    def get_correct_car_object(name):
        if name in cars_dict.keys():
            car = cars_dict[name]
        else:
            car = Car()
            car.restore(name)
        return car


cars_dict = {}

# while True:
#     creating = input("Создать говую машину: да/нет/удалить:").lower()
#     if creating == "да":
#         info = [input("Имя:"), input("Тип:"), 
#                 input("Производитель:"), input("Цвет:"), input("Привод:"), input("Коробка:"), input("Объём д:")]
#         car = Car(info[0], info[1], info[2], info[3], info[4], info[5], info[6])
#         cars_dict[info[0]] = car
#         print(car.get_info())
#     if creating == "удалить":
#         name = input("Имя:")
#         if name in cars_dict.keys():
#             car = cars_dict[name]
#             car.delete()
#             del cars_dict[name]
#     name = input("C какой машиной будем работать?:")
#     if name not in cars_dict.keys():
#         continue
#     car: Car = cars_dict[name]
#     action = input("Узнать данные: 1\nАктивировать поворотник: 2\nДеактивировать поворотник: 3\nОткрыть дверь: 4\nЗакрыть дверь: 5\nРедатировать параметры: 6\n")
#     if int(action) == 1:
#         print(car.get_info())
#     if int(action) == 2:
#         pos = input("Левый: 0/Правый 1")
#         car.activate_rotator(int(pos))
#     if int(action) == 3:
#         pos = input("Левый: 0/Правый 1")
#         car.deactivate_rotator(int(pos))
#     if int(action) == 4:
#         pos = input("Левая передняя: 0/Правая передняя: 1/Левая задняя: 2/Правая Задняя: 3")
#         car.open_door(int(pos))
#     if int(action) == 5:
#         pos = input("Левая передняя: 0/Правая передняя: 1/Левая задняя: 2/Правая Задняя: 3")
#         car.close_door(int(pos))
#     if int(action) == 6:
#         while True:
#             param = input("Введите параметр и значение:").split()
#             if param[0] == "color":
#                 car.color = param[1]
#             elif param[0] == "type":
#                 car.type = param[1]
#             elif param[0] == "box_type":
#                 car.box_type = param[1]
#             elif param[0] == "privod":
#                 car.privod = param[1]
#             elif param[0] == "v_engine":
#                 car.v_engine = param[1]
#             else:
#                 continue
#             car.save()
#             print(car.get_info())
#             break
            

