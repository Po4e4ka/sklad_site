from django.http import HttpResponse
from .models import Positions, Change_qantity
from datetime import datetime, timedelta
import logging


logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


def find_pos(data: str = False, code_pos: str = False):
    """
    Функция поиска данных в таблице Positions.
    На входе - два значения - в формате строк.
    Первая строка: наименование/ часть наименования.
    Вторая строка: штрих-код/ часть штрих кода.
    Если введен штрих-код -> перевод его в инт
    Если хоть один параметр поиска определен -> возвращает QuerySet (м.б. пустым)
    Если не введен ни один параметр выборки -> return HttpResponse("Bad Request: Parameters is not defined")
    """
    try:
        pos_find = Positions.objects.all()
        if code_pos:
            code_pos = int(code_pos)
        if data and not code_pos:
            return pos_find.filter(name__icontains=data)
        elif not data and code_pos:
            return pos_find.filter(code__icontains=code_pos)
        elif data and code_pos:
            return pos_find.filter(code__icontains=code_pos).filter(name__icontains=data)
        else:
            return HttpResponse("Bad Request: Parameters is not defined")
    except Exception as e:
        logging.error("Request parameters is not defined, %s", e)
        return HttpResponse("Bad Request")


def find_change(data1: datetime = False, data2: datetime = False, type: str = False):
    """
    Функция поиска данных в таблице Change_qantity.
    На входе - три значения - в формате строк.
    Первая строка: дата1.
    Вторая строка: дата2.
    Третья - тип операции
    Если хоть один параметр поиска определен -> возвращает QuerySet (м.б. пустым)
    """
    try:
        change_find = Change_qantity.objects.all()
        if data1 and not data2 and not type:
            res_date = change_find.filter(time_oper__startswith=data1)
            return res_date
        elif data2 and not type:
            prev_date = change_find.exclude(time_oper__gte=data2+timedelta(days=1))
            if data1 and prev_date:
                period_date = prev_date.filter(time_oper__gte=data1)
                return period_date
            else:
                return prev_date
        if type:
            type = int(type)
            pos_find_type = change_find.filter(change_type_id=type)
            if pos_find_type:
                if data1 and not data2:
                    res_date_type = pos_find_type.filter(time_oper__startswith=data1)
                    return res_date_type
                elif data1 and data2:
                    period_date_type = pos_find_type.exclude(time_oper__gte=data2+timedelta(days=1)).filter(time_oper__gte=data1)
                    return period_date_type
                if not data1 and data2:
                    res_date_type = pos_find_type.exclude(time_oper__gte=data2+timedelta(days=1))
                    return res_date_type
            else:
                return pos_find_type
    except Exception as e:
        logging.error("Request parameters is not defined, %s", e)
        return HttpResponse("Bad Request: Parameters is not defined")