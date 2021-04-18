from django.http import HttpResponse
from .models import Positions, Change_qantity
from datetime import datetime, timedelta
import logging


logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


def find_pos(data: str = False, code_pos: str = False):
    pos_find = Positions.objects.all()
    try:
        if data and not code_pos:
            pos_find_name = pos_find.filter(name__icontains=data)
            if pos_find_name:
                logging.info("Выбрано %s позиций", len(pos_find_name))
                return pos_find_name
            else:
                logging.info("По запросу %s позиций не найдено", str)
                return pos_find_name
        if code_pos:
            code_pos = int(code_pos)
        if not data and code_pos:
            pos_find_code = pos_find.filter(code__icontains=code_pos)
            if pos_find_code:
                logging.info("Выбрано %s позиций", len(pos_find_code))
                return pos_find_code
            else:
                logging.info("По запросу %s позиций не найдено", code_pos)
                return HttpResponse("Positions is absent")
        if data and code_pos:
            pos_find_all = pos_find.filter(code__icontains=code_pos).filter(name__icontains=data)
            if pos_find_all:
                logging.info("Выбрано %s позиций", len(pos_find_all))
                return pos_find_all
            else:
                logging.info("По запросу %s и %ы позиций не найдено", data, code_pos)
                return HttpResponse("Positions is absent")
    except Exception as e:
        logging.error("Request parameters is not defined, %s", e)
        return HttpResponse("Bad Request: Parameters is not defined")


def find_change(data1: datetime = False, data2: datetime = False, type: str = False):
    change_find = Change_qantity.objects.all()
    try:
        if data1 and not data2 and not type:
            res_date = change_find.filter(time_oper__startswith=data1)
            if res_date:
                logging.info("Выбрано %s позиций", len(res_date))
                return res_date
            else:
                logging.info("По запросу %s операций не найдено", data1)
                return HttpResponse("Change_qantity in this date is absent")
        elif data2 and not type:
            prev_date = change_find.exclude(time_oper__gte=data2+timedelta(days=1))
            if data1 and prev_date:
                period_date = prev_date.filter(time_oper__gte=data1)
                if period_date:
                    logging.info("Выбрано %s позиций", len(period_date))
                    return period_date
                else:
                    logging.info("По запросу в период %s, %s операций не найдено", data1, data2)
                    return HttpResponse("Change_qantity in this date is absent")
            elif not data1 and prev_date:
                logging.info("Выбрано %s позиций", len(prev_date))
                return prev_date
            else:
                logging.info("По запросу %s операций не найдено", data2)
                return HttpResponse("Change_qantity under this date is absent")
        if type:
            type = int(type)
            pos_find_type = change_find.filter(change_type_id=type)
            if pos_find_type:
                if data1 and not data2:
                    res_date_type = pos_find_type.filter(time_oper__startswith=data1)
                    if res_date_type:
                        logging.info("Выбрано %s позиций", len(res_date_type))
                        return res_date_type
                    else:
                        logging.info("По запросу %s и типу операций %s не найдено", data1, type)
                        return HttpResponse("Change_qantity in this date is absent")
                if data1 and data2:
                    period_date_type = pos_find_type.exclude(time_oper__gte=data2+timedelta(days=1)).filter(time_oper__gte=data1)
                    if period_date_type:
                        logging.info("Выбрано %s позиций", len(period_date_type))
                        return period_date_type
                    else:
                        logging.info("По запросу %s, %s и типу операций %s не найдено", data1, data2, type)
                        return HttpResponse("Change_qantity in this date is absent")
                if not data1 and data2:
                    res_date_type = pos_find_type.exclude(time_oper__gte=data2+timedelta(days=1))
                    if res_date_type:
                        logging.info("Выбрано %s позиций", len(res_date_type))
                        return res_date_type
                    else:
                        logging.info("По запросу до %s и типу операций %s не найдено", data2, type)
                        return HttpResponse("Change_qantity under this date is absent")
            else:
                logging.info("По типу %s операций не найдено", type)
                return HttpResponse("Change_qantity on this type is absent")
    except Exception as e:
        logging.error("Request parameters is not defined, %s", e)
        return HttpResponse("Bad Request: Parameters is not defined")