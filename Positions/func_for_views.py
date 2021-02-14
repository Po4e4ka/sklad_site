# from django.db.models import Max, Avg
from django.forms import model_to_dict
from django.http import HttpResponse
from .models import Positions, Groups, Xyz, Levels, Persons, Objects, \
    Change_types, Change_qantity
import pandas as pd
from datetime import datetime


def excel_to_dict(file="Positions/Копия 1.xls"):
    # Load spreadsheet
    xl = pd.ExcelFile(file)
    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse('номенклатура')
    result = []
    for index, row in df1.iterrows():
        if type(row['номенклатура']) == float:
            break
        result.append({"name": row['номенклатура'], "quantity": row["количество"], "ediz": row["ед.измер."]})
    return result


def data_test(data):
    if type(data) != dict:
        return HttpResponse("Bad Request: wrong type of data")


def vvod_info_pos(data: dict):
    data_test(data)
    if "name" in data:
        if Positions.objects.filter(name=data["name"]).count() > 0:
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: positions.name is already in base")
        else:
            try:
                position = Positions(**data)
                position.save()
                print(f"Сохранено в базе: {position.id}, {position.name}, {position.quantity}")
                vvod_info_ch_qant(data, type=5)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: positions.name is absent")


nomenklatura_test = [{"id": 1, "name": "материалы"},
                     {"id": 2, "name": "комплектующие и детали"},
                     {"id": 3, "name": "запасные части"},
                     {"id": 4, "name": "разное"}]


def vvod_info_group(data: dict):
    data_test(data)
    if "name" in data:
        if Groups.objects.filter(name=data["name"]).count() > 0:
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: group.name is already in base")
        else:
            try:
                group = Groups(**data)
                group.save()
                print(f"Сохранено в базе: {group.id}, {group.name}")
                vvod_info_ch_qant(data, type=5)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: group.name is absent")


xyz_test = [{"id": 1, "X": "a", "y": 1, "z": 1},
            {"id": 2, "X": "a", "y": 2, "z": 1},
            {"id": 3, "X": "a", "y": 3, "z": 1}]


def vvod_info_xyz(data: dict):
    """доделать другую проверку - чтобы выбиралось из закрытого перечня координат"""
    data_test(data)
    if "X" and "y" not in data:
        print("Координаты не определены, введите параметры: x - латинские буквы от A до Z, y - число от 1 до 9")
        return HttpResponse("Bad Request: xyz.X and xyz.y is not defined")
    else:
        try:
            xyz = Xyz(**data)
            xyz.save()
            print(f"Сохранено в базе: {xyz.id}, {xyz.X}, {xyz.z}")
            vvod_info_ch_qant(data, type=5)
        except:
            return -1
        else:
            return HttpResponse("Bad Request: group.id is not defined")


level_test = [{"id": 1, "name": "top"},
              {"id": 2, "name": "buh"},
              {"id": 3, "name": "sklad"},
              {"id": 4, "name": "another"},
              {"id": 5, "name": "admin"}
              ]


def vvod_info_level(data: dict):
    data_test(data)
    """доделать другую проверку - добавлять уровни только админу"""
    if "name" in data:
        if Levels.objects.filter(name=data["name"]).count() > 0:
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: levels.name is already in base")
        else:
            try:
                level = Levels(**data)
                level.save()
                print(f"Сохранено в базе: {level.id}, {level.name}")
                vvod_info_ch_qant(data, type=5)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: level.name is not defined")


person_test = [{"id": 1, "name": "Иванов Иван"},
               {"id": 2, "name": "Петров Петр"},
               {"id": 3, "name": "Сидоров Сидор"},
               {"id": 4, "name": "Инкогнито"}]


def vvod_info_person(data: dict):
    data_test(data)
    if "name" in data:
        if Persons.objects.filter(name=data["name"]).count() > 0:
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: persons.name is already in base")
        else:
            try:
                person = Persons(**data)
                person.save()
                print(f"Сохранено в базе: {person.id}, {person.name}")
                vvod_info_ch_qant(data, type=5)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: person.name is absent")


obj_test = [
    {"id": 1, "name": "object1"},
    {"id": 2, "name": "object2"},
    {"id": 3, "name": "object3"},
]


def vvod_info_obj(data: dict):
    data_test(data)
    if "name" in data:
        if Objects.objects.filter(name=data["name"]).count() > 0:
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: objects.name is already in base")
        else:
            try:
                obj = Objects(**data)
                obj.save()
                print(f"Сохранено в базе: {obj.id}, {obj.name}")
                vvod_info_ch_qant(data, type=5)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: objects.name is not defined")


change_test = [
    {"id": 1, "name": "prihod", "znak": False},
    {"id": 2, "name": "rashod", "znak": True},
    {"id": 3, "name": "izlishki", "znak": False},
    {"id": 4, "name": "nedostacha", "znak": True},
]


def vvod_info_ch_type(data: dict):
    """закрытый перечень операций, права изменения только у админа"""
    data_test(data)
    if "name" in data:
        if Change_types.objects.filter(name=data["name"]).count() > 0:
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: change_types.name is already in base")
        else:
            try:
                ch_type = Change_types(**data)
                ch_type.save()
                print(f"Сохранено в базе: {ch_type.id}, {ch_type.name}")
                vvod_info_ch_qant(data, type=5)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: change_types.name is not defined")


qant_test = {"position_id": Positions.objects.filter(id=3).get().id, "quantity": 300.0}
type_test = 4


def vvod_info_ch_qant(data: dict = qant_test, type=type_test):
    data_test(data)
    # print(data)
    if type < 5:
        if Positions.objects.filter(id=data["position_id"]).count() < 1:
            print("Позиция не найдена", data["position_id"])
            return HttpResponse("Bad Request: Positions.id is not defined")
        ch_qant = Change_qantity()
        ch_qant.time_oper = datetime.now()
        ch_qant.change_type_id = Change_types.objects.filter(id=type).get()
        ch_qant.position_id = Positions.objects.filter(id=data["position_id"]).get()
        ch_qant.quantity = data["quantity"]

        print(model_to_dict(ch_qant))
        ch_qant.save()

        pos = Positions.objects.filter(id=data["position_id"]).get()
        # print(Change_types.objects.filter(id=type).get().znak)
        pos.quantity += (-1) ** Change_types.objects.filter(id=type).get().znak * data["quantity"]
        pos.save()
        print(pos.quantity)
        print(f"Сохранено в базе: {pos.id},{pos.name}, {pos.quantity}")

    else:
        print("записана операция с нулевым изменением количества")
        # ch_qant = Change_qantity(**data)
        # ch_qant.time_oper = datetime.now()
        # ch_qant.save()
        # print(model_to_dict(ch_qant))