from datetime import datetime, timedelta
import logging
from django.http import HttpResponse
from .models import Change_qantity


logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)



def otchet_obj(id_obj :int, data1 : datetime = False, data2: datetime = False):
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
            prev_date = change_find.exclude(time_oper__gte=data2 + timedelta(days=1))
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
                    period_date_type = pos_find_type.exclude(time_oper__gte=data2 + timedelta(days=1)).filter(
                        time_oper__gte=data1)
                    if period_date_type:
                        logging.info("Выбрано %s позиций", len(period_date_type))
                        return period_date_type
                    else:
                        logging.info("По запросу %s, %s и типу операций %s не найдено", data1, data2, type)
                        return HttpResponse("Change_qantity in this date is absent")
                if not data1 and data2:
                    res_date_type = pos_find_type.exclude(time_oper__gte=data2 + timedelta(days=1))
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