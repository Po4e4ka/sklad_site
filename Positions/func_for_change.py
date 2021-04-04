from .func_for_views import vvod_info_ch_qant, data_test
from django.http import HttpResponse
from .models import Positions, Change_types
import logging
from .sklad_exceptions import DataTypeError

logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


def change_info_pos(data: dict):
    try:
        if data_test(data):
            pos_all = Positions.objects.all()
            if pos_all.filter(id=data["id"]).exists():
                rec_pos = pos_all.filter(id=data["id"]).get()
                if "name" in data:
                    if data['name'] != rec_pos.name:
                        if pos_all.filter(name=data['name']).exists():
                            logging.error("Position.name %s is already in Base", data['name'])
                            return DataTypeError
                        else:
                            rec_pos.name = data['name']
                if "quantity" in data:
                    rec_pos.quantity = float(data["quantity"])
                if "code" in data:
                    rec_pos.code = int(data['code'])
                if "ediz" in data:
                    rec_pos.ediz = data['ediz']
                rec_pos.save()
                print(f"Сохранено в базе: {rec_pos.id}, {rec_pos.name}, {rec_pos.quantity}")
                vvod_info_ch_qant(data, type=5)
            else:
                print(f"Id {data['id']} не найден")
                return HttpResponse("Bad Request: positions.id is absent")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Change_info_pos is not saved %s", e)
        return HttpResponse("Bad Request: Change_info_pos is not saved")


def change_info_ch_type(data: dict):
    try:
        if data_test(data):
            ch_type_all = Change_types.objects.all()
            if ch_type_all.filter(id=data["id"]).exists():
                rec_ch_type = ch_type_all.filter(id=data["id"]).get()
                if "name" in data:
                    if data['name'] != rec_ch_type.name:
                        if ch_type_all.filter(name=data['name']).exists():
                            logging.error("Change_types.name %s is already in Base", data['name'])
                            return DataTypeError
                        else:
                            rec_ch_type.name = data['name']
                if "znak" in data:
                    rec_ch_type.znak = data['znak']
                rec_ch_type.save()
                logging.info("Изменено в базе: %s, %s", rec_ch_type.id, rec_ch_type.name)
                vvod_info_ch_qant(data, type=11)
            else:
                logging.info("Обязательный атрибут id не определен")
                return HttpResponse("Bad Request: ch_type.id is absent")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except Exception as e:
        logging.error("Change_info_ch_type is not saved %s", e)
        return HttpResponse("Bad Request: Change_info_ch_type is not saved")