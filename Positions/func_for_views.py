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
        if Positions.objects.filter(name=data["name"]).exists():
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
        if Groups.objects.filter(name=data["name"]).exists():
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: group.name is already in base")
        else:
            try:
                group = Groups(**data)
                group.save()
                print(f"Сохранено в базе: {group.id}, {group.name}")
                vvod_info_ch_qant(data, type=6)
            except:
                return -1
    else:
        return HttpResponse("Bad Request: group.name is absent")


xyz_test = [{"X": "a", "y": 1, "z": 1},
            {"X": "a", "y": 2, "z": 1},
            {"X": "a", "y": 3}]


def vvod_info_xyz(data: dict):
    """доделать другую проверку - чтобы выбиралось из закрытого перечня координат"""
    data_test(data)
    if "X" and "y" not in data:
        print("Координаты не определены, введите параметры: x - латинские буквы от A до Z, y - число от 1 до 9")
        return HttpResponse("Bad Request: xyz.X and xyz.y is not defined")
    else:
        try:
            if "z" not in data and Xyz.objects.filter(X=data["X"], y=data["y"]).exists():
                print(f"Есть в базе {data['X']}, {data['y']}")
                return HttpResponse("Bad Request: Xyz.name is already in base")
            elif "z" in data and Xyz.objects.filter(X=data["X"], y=data["y"], z=data["z"]).exists():
                print(f"Есть в базе {data['X']}, {data['y']}, {data['z']}")
                return HttpResponse("Bad Request: Xyz.name is already in base")
            else:
                xyz = Xyz(**data)
                xyz.save()
                print(f"Сохранено в базе: {xyz.id}, {xyz.X}, {xyz.y}, {xyz.z}")
                vvod_info_ch_qant(data, type=7)
        except:
            return -1


level_test = [{"name": "top"},
              {"name": "buh"},
              {"name": "sklad"},
              {"name": "another"},
              {"name": "admin"}]


def vvod_info_level(data: dict):
    data_test(data)
    """доделать другую проверку - добавлять уровни только админу"""
    if "name" in data:
        if Levels.objects.filter(name=data["name"]).exists():
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: levels.name is already in base")
        else:
            try:
                level = Levels(**data)
                level.save()
                print(f"Сохранено в базе: {level.id}, {level.name}")
                vvod_info_ch_qant(data, type=8)
            except Exception as e:
                print(e)
    else:
        return HttpResponse("Bad Request: level.name is not defined")


person_test = [{"name": "Иванов Иван"},
               {"name": "Петров Петр"},
               {"name": "Сидоров Сидор"},
               {"name": "Михайлов Алексей"}]


def vvod_info_person(data: dict):
    data_test(data)
    if "name" in data:
        if Persons.objects.filter(name=data["name"]).exists():
            print("Есть в базе", data["name"])
            return HttpResponse("Bad Request: persons.name is already in base")
        else:
            try:
                person = Persons(**data)
                person.save()
                print(f"Сохранено в базе: {person.id}, {person.name}")
                vvod_info_ch_qant(data, type=9)
            except Exception as e:
                print(e)
    else:
        return HttpResponse("Bad Request: person.name is absent")


obj_test = [{"name": "object1"},
    {"name": "object2"},
    {"name": "object0"}]


def vvod_info_obj(data: dict):
    data_test(data)
    if "name" in data:
        if Objects.objects.filter(name=data["name"]).exists():
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: objects.name is already in base")
        else:
            try:
                obj = Objects(**data)
                obj.save()
                print(f"Сохранено в базе: {obj.id}, {obj.name}")
                vvod_info_ch_qant(data, type=10)
            except Exception as e:
                print(e)
    else:
        return HttpResponse("Bad Request: objects.name is not defined")


change_test = [{"name": "prihod", "znak": False},
    {"name": "rashod", "znak": True},
    {"name": "izlishki", "znak": False},
    {"name": "nedostacha", "znak": True}]


def vvod_info_ch_type(data: dict):
    """закрытый перечень операций, права изменения только у админа"""
    data_test(data)
    if "name" in data:
        if Change_types.objects.filter(name=data["name"]).exists():
            print(f"Есть в базе {data['name']}")
            return HttpResponse("Bad Request: change_types.name is already in base")
        else:
            try:
                ch_type = Change_types(**data)
                ch_type.save()
                print(f"Сохранено в базе: {ch_type.id}, {ch_type.name}")
                vvod_info_ch_qant(data, type=11)
            except Exception as e:
                print(e)
    else:
        return HttpResponse("Bad Request: change_types.name is not defined")


qant_test = {"position_id": Positions.objects.filter(id=1).get().id, "quantity": 100.0}
type_test = 2


def vvod_info_ch_qant(data: dict = qant_test, type=type_test):
    data_test(data)
    # print(data)
    ch_qant = Change_qantity()
    ch_qant.time_oper = datetime.today()
    if type < 5:
        if not Positions.objects.filter(id=data["position_id"]).exists():
            print("Позиция не найдена", data["position_id"])
            return HttpResponse("Bad Request: Positions.id is not defined")

        ch_qant.change_type_id = Change_types.objects.filter(id=type).get()
        ch_qant.position_id = Positions.objects.filter(id=data["position_id"]).get()
        ch_qant.quantity = data["quantity"]

        pos = Positions.objects.filter(id=data["position_id"]).get()
        # print(Change_types.objects.filter(id=type).get().znak)
        pos.quantity += (-1) ** Change_types.objects.filter(id=type).get().znak * data["quantity"]
        pos.save()
        print(pos.quantity)
        print(f"Сохранено в базе: {pos.id},{pos.name}, {pos.quantity}")

    else:
        print("записана операция с нулевым изменением количества")
        ch_qant.change_type_id = Change_types.objects.filter(id=5).get()
    ch_qant.save()
    print(model_to_dict(ch_qant))