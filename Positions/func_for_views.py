# from django.db.models import Max, Avg
import random

from django.forms import model_to_dict
from django.http import HttpResponse
from .models import Positions, Groups, Xyz, Levels, Persons, Objects, Change_types, Change_qantity
import pandas as pd
from datetime import datetime
import logging
from .sklad_exceptions import DataTypeError

# filemode="w"


logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


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
        return False
    else:
        return True


def vvod_info_pos(data):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Positions.name is absent")
                return HttpResponse("Bad Request: positions.name is absent")

            try:
                if Positions.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: positions.name is already in base")
                else:
                    position = Positions(**data)
                    if "quantity" not in data:
                        position.quantity = 0.0
                    if "mol" not in data:
                        position.mol = Persons.objects.filter(id=random.randint(1,5)).get()  # доделать генерацию
                    position.save()
                    logging.info("Сохранено в базе %s, %s, %s", position.id, position.name, position.quantity)
                    vvod_info_ch_qant(data, 5)
            except Exception as e:
                logging.error("Positions is not saved %s", e)
                return HttpResponse("Bad Request: Positions is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")


nomenklatura_test = [{"name": "материалы"},
                     {"name": "комплектующие и детали"},
                     {"name": "запасные части"},
                     {"name": "оборудование"}]


def vvod_info_group(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Group.name is absent")
                return HttpResponse("Bad Request: group.name is absent")

            try:
                if Groups.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: group.name is already in base")
                else:
                    group = Groups(**data)
                    group.save()
                    logging.info("Сохранено в базе %s, %s", group.id, group.name)
                    vvod_info_ch_qant(data, 6)
            except Exception as e:
                logging.error("Groups is not saved %s", e)
                return HttpResponse("Bad Request: Groups is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")

xyz_test = [{"X": "a", "y": 1, "z": 1},
            {"X": "a", "y": 2, "z": 1},
            {"X": "a", "y": 3, "z": 5},
            {"X": "a", "y": 3, "z": 4}]


def vvod_info_xyz(data: dict):
    """доделать другую проверку - чтобы выбиралось из закрытого перечня координат"""
    try:
        if data_test(data):
            try:
                if "X" not in data or "y" not in data:
                    logging.info("Обязательные координаты X и y - не определены")
                    return HttpResponse("Bad Request: xyz.X and xyz.y is not defined")
                elif "z" not in data and Xyz.objects.filter(X=data["X"], y=data["y"], z="null").exists():
                    logging.info("Есть в базе %s, %s", data['X'], data['y'])
                    return HttpResponse("Bad Request: Xyz.name is already in base")
                elif Xyz.objects.filter(X=data["X"], y=data["y"], z=data["z"]).exists():
                    logging.info("Есть в базе %s, %s, %s", data['X'], data['y'], data['z'])
                    return HttpResponse("Bad Request: Xyz.name is already in base")
                else:
                    xyz = Xyz(**data)
                    xyz.save()
                    logging.info("Сохранено в базе %s, %s, %s", xyz.id, xyz.X, xyz.y, xyz.z)
                    vvod_info_ch_qant(data, 7)
            except Exception as e:
                logging.error("Groups is not saved %s", e)
                return HttpResponse("Bad Request: Xyz is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")


level_test = [{"name": "top"},
              {"name": "buh"},
              {"name": "sklad"},
              {"name": "another"},
              {"name": "admin"}]


def vvod_info_level(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Levels.name is absent")
                return HttpResponse("Bad Request: level.name is not defined")
            try:
                if Levels.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: levels.name is already in base")
                else:
                    level = Levels(**data)
                    level.save()
                    logging.info("Сохранено в базе: %s, %s", level.id, level.name)
                    vvod_info_ch_qant(data, 8)
            except Exception as e:
                logging.error("Levels is not saved %s", e)
                return HttpResponse("Bad Request: Levels is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")


person_test = [{"name": "Иванов Иван"},
               {"name": "Петров Петр"},
               {"name": "Сидоров Сидор"},
               {"name": "Михайлов Алексей"}]


def vvod_info_person(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Persons.name is absent")
                return HttpResponse("Bad Request: person.name is absent")
            try:
                if Persons.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data["name"])
                    return HttpResponse("Bad Request: persons.name is already in base")
                else:
                    person = Persons(**data)
                    person.save()
                    logging.info("Сохранено в базе: %s, %s", person.id, person.name)
                    vvod_info_ch_qant(data, 9)
            except Exception as e:
                logging.error("Persons is not saved %s", e)
                return HttpResponse("Bad Request: Persons is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")


obj_test = ["object8", "object9"]


def vvod_info_obj(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Objects.name is absent")
                return HttpResponse("Bad Request: objects.name is not defined")
            try:
                if Objects.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: objects.name is already in base")
                else:
                    obj = Objects(**data)
                    obj.save()
                    logging.info("Сохранено в базе: %s, %s", obj.id, obj.name)
                    vvod_info_ch_qant(data, 10)
            except Exception as e:
                logging.error("Objects is not saved %s", e)
                return HttpResponse("Bad Request: Objects is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")


change_test = ["vvod_info_ch_type_new"]


def vvod_info_ch_type(data: dict):
    """закрытый перечень операций, права изменения только у админа"""
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Change_types.name is absent")
                return HttpResponse("Bad Request: change_types.name is not defined")

            try:
                if Change_types.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: change_types.name is already in base")
                else:
                    ch_type = Change_types(**data)
                    ch_type.save()
                    logging.info("Сохранено в базе: %s, %s", ch_type.id, ch_type.name)
                    vvod_info_ch_qant(data, 11)
            except Exception as e:
                logging.error("Change_types is not saved %s", e)
                return HttpResponse("Bad Request: Change_types is not saved")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")

# qant_test = {"position_id": Positions.objects.filter(id=1).get().id, "quantity": 100.0}
# type_test = 2


def vvod_info_ch_qant(data: dict, type):
    try:
        if data_test(data):
            ch_qant = Change_qantity()
            ch_qant.time_oper = datetime.today()
            try:
                if type < 5:
                    if not Positions.objects.filter(id=data["position_id"]).exists():
                        logging.info("Позиция %s не найдена ", data["position_id"])
                        return HttpResponse("Bad Request: Positions.id is not defined")
                    else:
                        ch_qant.change_type_id = Change_types.objects.filter(id=type).get()
                        ch_qant.position_id = Positions.objects.filter(id=data["position_id"]).get()
                        if "quantity" in data:
                            ch_qant.quantity = data["quantity"]
                        else:
                            ch_qant.quantity = 0.0

                        pos = Positions.objects.filter(id=data["position_id"]).get()
                        pos.quantity += (-1) ** Change_types.objects.filter(id=type).get().znak * data["quantity"]
                        pos.save()
                        logging.info("Сохранено в базе: %s, %s, %s", pos.id, pos.name, pos.quantity)
                else:
                    ch_qant.change_type_id = Change_types.objects.filter(id=type).get()
                    logging.info("записана операция с нулевым изменением количества, тип %s, %s", type, Change_types.objects.filter(id=type).get().name)
                # if "person_id_mol" not in data:
                #     ch_qant.person_id_mol = Persons.objects.filter(id=random.randint(1, 5)).get() # доделать генерацию
                # if "person_id_contr" not in data:
                #     ch_qant.person_id_contr = Persons.objects.filter(id=random.randint(1, 5)).get()  # доделать генерацию
            except Exception as e:
                logging.error("Change_qantity is not saved %s", e)
                return HttpResponse("Bad Request: Change_qantity is not saved")
            ch_qant.save()
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")