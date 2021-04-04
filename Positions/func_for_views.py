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


def vvod_info_pos(data):
    """
    Функция ввода в таблицу Positions.
    На входе - словарь, у которого все значения - в формате строк.
    Если в поданных данных нет атрибута "name" -> return HttpResponse("Bad Request: positions.name is absent")
    Если введенное наименование уже есть в перечне позиций ->
    1. Запись в журнале - позиция уже есть в списке.
    2. return HttpResponse("Bad Request: positions.name is already in base")
    В случае успешного ввода новой позиции ->
    1. Если количество не определено -> в графе "quantity" по умолчанию присваивается значение 0.
    2. Запись в журнале - Сохранено в базе ИД, наименование, количество.
    3. Запись в таблице Change_qantity (с типом операции 5).
    """
    try:
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
    except Exception as e:
        logging.error("Positions is not saved %s", e)
        return HttpResponse("Bad Request: Positions is not saved")


def vvod_info_group(data: dict):
    """
        Функция ввода в таблицу Group.
        На входе - словарь, у которого все значения - в формате строк.
        Если в поданных данных нет атрибута "name" -> return HttpResponse("Bad Request: group.name is absent")
        Если введенное наименование уже есть в перечне позиций ->
        1. Запись в журнале - позиция уже есть в списке.
        2. return HttpResponse("Bad Request: group.name is already in base")
        В случае успешного ввода новой позиции ->
        1. Запись в журнале - Сохранено в базе ИД, наименование.
        2. Запись в таблице Change_qantity (с типом операции 6).
    """
    try:
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
    except Exception as e:
        logging.error("Groups is not saved %s", e)
        return HttpResponse("Bad Request: Groups is not saved")


def vvod_info_xyz(data: dict):
    """
    Функция ввода в таблицу Xyz.
    На входе - словарь, у которого все значения - в формате строк.
    Если в поданных данных нет двух обязательных атрибутов "X" и "y" -> return HttpResponse("Bad Request: Bad Request: xyz.X and xyz.y is not defined")
    Если в поданных значениях не определна координа "z" (высота) -> по умолчанию присваивается z = 1
    Если набор координат (X, y, z) уже есть в перечне позиций ->
    1. Запись в журнале - позиция уже есть в списке.
    2. return HttpResponse("Bad Request: Xyz is already in base")
    В случае успешного ввода новой позиции ->
    1. Запись в журнале - Сохранено в базе ИД, X, y, z.
    2. Запись в таблице Change_qantity (с типом операции 7).
    """
    try:
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
                return HttpResponse("Bad Request: Xyz is already in base")
            else:
                xyz = Xyz(**data)
                xyz.save()
                logging.info("Сохранено в базе %s, %s, %s, %s", xyz.id, xyz.X, xyz.y, xyz.z)
                vvod_info_ch_qant(data, 7)
    except Exception as e:
            logging.error("Groups is not saved %s", e)
            return HttpResponse("Bad Request: Xyz is not saved")


def vvod_info_level(data: dict):
    """
    Функция ввода в таблицу Levels.
    На входе - словарь, у которого все значения - в формате строк.
    Если в поданных данных нет атрибута "name" -> return HttpResponse("Bad Request: level.name is absent")
    Если введенное наименование уже есть в перечне позиций ->
    1. Запись в журнале - позиция уже есть в списке.
    2. return HttpResponse("Bad Request: levels.name is already in base")
    В случае успешного ввода новой позиции ->
    1. Запись в журнале - Сохранено в базе ИД, наименование.
    2. Запись в таблице Change_qantity (с типом операции 8).
        """
    try:
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
    except Exception as e:
        logging.error("Levels is not saved %s", e)
        return HttpResponse("Bad Request: Levels is not saved")


def vvod_info_person(data: dict):
    """
    Функция ввода в таблицу Persons.
    На входе - словарь, у которого все значения - в формате строк.
    Если в поданных данных нет атрибута "name" -> return HttpResponse("Bad Request: person.name is absent")
    Если введенное наименование уже есть в перечне позиций ->
    1. Запись в журнале - позиция уже есть в списке.
    2. return HttpResponse("Bad Request: persons.name is already in base")
    В случае успешного ввода новой позиции ->
    1. Запись в журнале - Сохранено в базе ИД, наименование.
    2. Запись в таблице Change_qantity (с типом операции 9).
    """
    try:
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
    except Exception as e:
        logging.error("Persons is not saved %s", e)
        return HttpResponse("Bad Request: Persons is not saved")


def vvod_info_obj(data: dict):
    """
    Функция ввода в таблицу Objects.
    На входе - словарь, у которого все значения - в формате строк.
    Если в поданных данных нет атрибута "name" -> return HttpResponse("Bad Request: objects.name is absent")
    Если введенное наименование уже есть в перечне позиций ->
    1. Запись в журнале - позиция уже есть в списке.
    2. return HttpResponse("Bad Request: objects.name is already in base")
    В случае успешного ввода новой позиции ->
    1. Запись в журнале - Сохранено в базе ИД, наименование.
    2. Запись в таблице Change_qantity (с типом операции 10).
    """
    try:
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
    except Exception as e:
        logging.error("Objects is not saved %s", e)
        return HttpResponse("Bad Request: Objects is not saved")


def vvod_info_ch_type(data: dict):
    """
    Функция ввода в таблицу Change_types.
    На входе - словарь, у которого все значения - в формате строк.
    Если в поданных данных нет атрибута "name" -> return HttpResponse("Bad Request: change_types.name is absent")
    Если введенное наименование уже есть в перечне позиций ->
    1. Запись в журнале - позиция уже есть в списке.
    2. return HttpResponse("Bad Request: change_types.name is already in base")
    В случае успешного ввода новой позиции ->
    1. Запись в журнале - Сохранено в базе ИД, наименование.
    2. Запись в таблице Change_qantity (с типом операции 11).
    """
    try:
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
    except Exception as e:
        logging.error("Change_types is not saved %s", e)
        return HttpResponse("Bad Request: Change_types is not saved")


def vvod_info_ch_qant(data: dict, type):
    """
    Функция ввода в таблицу Change_qantity.
    На входе - словарь, у которого все значения - в формате строк.
    Если количество не определено -> в графе "quantity" по умолчанию присваивается значение 0.
    Если тип операции предполагает изменение количества -> поиск в таблице Positions позиции по position_id.
    Если не найдена позиция -> return HttpResponse("Bad Request: Positions.id is not defined")
    Если найдена позиция ->
    1. Изменение количества в таблице Positions.
    2.Запись в журнале - Сохранено в базе ИД, наименование, увеличено/ уменьшено на ..., остаток...
    Если операция ез изменения количества -> запись в журнале - записана операция с нулевым изменением количества, тип.
    """
    try:
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
    except Exception as e:
        logging.error("Change_qantity is not saved %s", e)
        return HttpResponse("Bad Request: Change_qantity is not saved")