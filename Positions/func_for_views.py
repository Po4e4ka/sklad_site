# from django.db.models import Max, Avg
import random
from django.forms import model_to_dict
from django.http import HttpResponse
from .models import Positions, Groups, Xyz, Levels, Persons, Objects, Change_types, Change_qantity
import pandas as pd
from datetime import datetime
import logging
from .sklad_exceptions import DataTypeError, data_test, IntTypeError, PeriodTypeError


logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


def excel_to_dict(file="for_test/Копия 1.xls"):
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


def vvod_info_pos(data):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Positions.name is absent")
                return HttpResponse("Bad Request: positions.name is absent")
            if Positions.objects.filter(name=data["name"]).exists():
                logging.info("Есть в базе %s", data['name'])
                return HttpResponse("Bad Request: positions.name is already in base")
            else:
                if "quantity" not in data:
                    data['quantity'] = 0.0
                else:
                    data['quantity'] = float(data['quantity'])
                if "code" in data:
                    data['code'] = int(data['code'])
                position = Positions(**data)
                position.save()
                logging.info("Сохранено в базе %s, %s, %s", position.id, position.name, position.quantity)
                vvod_info_ch_qant(data, 5)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Positions is not saved %s", e)
        return HttpResponse("Bad Request: Positions is not saved")


def vvod_info_group(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Group.name is absent")
                return HttpResponse("Bad Request: group.name is absent")
            else:
                if Groups.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: group.name is already in base")
                else:
                    group = Groups(**data)
                    group.save()
                    logging.info("Сохранено в базе %s, %s", group.id, group.name)
                    vvod_info_ch_qant(data, 6)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Groups is not saved %s", e)
        return HttpResponse("Bad Request: Groups is not saved")


def vvod_info_xyz(data: dict):
    """доделать дополнительную проверку - чтобы выбиралось из закрытого перечня координат"""
    try:
        if data_test(data):
            if "X" not in data or "y" not in data:
                logging.info("Обязательные координаты X и y - не определены")
                return HttpResponse("Bad Request: xyz.X and xyz.y is not defined")
            else:
                res_xyz = Xyz.objects.all()
                if "z" not in data:
                    data["z"] = 1
                else:
                    data["z"] = int(data["z"])
                data["y"] = int(data["y"])
                if res_xyz.filter(X=data["X"], y=data["y"], z=data["z"]).exists():
                    logging.info("Есть в базе %s, %s, %s", data['X'], data['y'], data['z'])
                    return HttpResponse("Bad Request: Xyz.name is already in base")
                else:
                    xyz = Xyz(**data)
                    xyz.save()
                    logging.info("Сохранено в базе %s, %s, %s, %", xyz.id, xyz.X, xyz.y, xyz.z)
                    vvod_info_ch_qant(data, 7)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
            logging.error("Groups is not saved %s", e)
            return HttpResponse("Bad Request: Xyz is not saved")


def vvod_info_level(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Levels.name is absent")
                return HttpResponse("Bad Request: level.name is not defined")
            else:
                if Levels.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: levels.name is already in base")
                else:
                    level = Levels(**data)
                    level.save()
                    logging.info("Сохранено в базе: %s, %s", level.id, level.name)
                    vvod_info_ch_qant(data, 8)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Levels is not saved %s", e)
        return HttpResponse("Bad Request: Levels is not saved")


def vvod_info_person(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Persons.name is absent")
                return HttpResponse("Bad Request: person.name is absent")
            else:
                if Persons.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data["name"])
                    return HttpResponse("Bad Request: persons.name is already in base")
                else:
                    if "phone" in data:
                        data["phone"] = int(data["phone"])
                    person = Persons(**data)
                    person.save()
                    logging.info("Сохранено в базе: %s, %s", person.id, person.name)
                    vvod_info_ch_qant(data, 9)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Persons is not saved %s", e)
        return HttpResponse("Bad Request: Persons is not saved")


def vvod_info_obj(data: dict):
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Objects.name is absent")
                return HttpResponse("Bad Request: objects.name is not defined")
            else:
                if Objects.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: objects.name is already in base")
                else:
                    obj = Objects(**data)
                    obj.save()
                    logging.info("Сохранено в базе: %s, %s", obj.id, obj.name)
                    vvod_info_ch_qant(data, 10)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Objects is not saved %s", e)
        return HttpResponse("Bad Request: Objects is not saved")


def vvod_info_ch_type(data: dict):
    """закрытый перечень операций, права изменения только у админа"""
    try:
        if data_test(data):
            if "name" not in data:
                logging.info("Change_types.name is absent")
                return HttpResponse("Bad Request: change_types.name is not defined")
            else:
                if Change_types.objects.filter(name=data["name"]).exists():
                    logging.info("Есть в базе %s", data['name'])
                    return HttpResponse("Bad Request: change_types.name is already in base")
                else:
                    ch_type = Change_types(**data)
                    ch_type.save()
                    logging.info("Сохранено в базе: %s, %s", ch_type.id, ch_type.name)
                    vvod_info_ch_qant(data, 11)
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Change_types is not saved %s", e)
        return HttpResponse("Bad Request: Change_types is not saved")


def vvod_info_ch_qant(data: dict, type):
    try:
        if data_test(data):
            ch_qant = Change_qantity()
            ch_qant.time_oper = datetime.today()
            if "quantity" in data:
                ch_qant.quantity = float(data["quantity"])
            else:
                ch_qant.quantity = 0.0
            ch_type_rec = Change_types.objects.filter(id=type).get()
            ch_qant.change_type_id = ch_type_rec

            if type not in (5, 6, 7, 8, 9, 10, 11):
                pos_all = Positions.objects.all()
                if not pos_all.filter(id=data["position_id"]).exists():
                    logging.info("Позиция %s не найдена ", data["position_id"])
                    return HttpResponse("Bad Request: Positions.id is not defined")
                else:
                    ch_qant.position_id = pos_all.filter(id=data["position_id"]).get()
                    pos = pos_all.filter(id=data["position_id"]).get()
                    pos.quantity += (-1) ** ch_type_rec.znak * float(data["quantity"])
                    pos.save()
                    logging.info("Сохранено в базе: %s, %s, %s, (True - уменьшено на, False - увеличено на) %s, остаток %s  единиц", pos.id, pos.name, ch_type_rec.znak, ch_qant.quantity, pos.quantity)
            else:
                logging.info("записана операция с нулевым изменением количества, тип %s, %s", type, Change_types.objects.filter(id=type).get().name)
            ch_qant.save()
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Change_qantity is not saved %s", e)
        return HttpResponse("Bad Request: Change_qantity is not saved")