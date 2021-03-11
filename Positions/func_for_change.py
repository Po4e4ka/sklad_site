from .func_for_views import vvod_info_ch_qant, data_test
from django.http import HttpResponse
from .models import Positions, Change_types
import logging

from .sklad_exceptions import DataTypeError

logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


new_pos = {"id": 1, "name": "материалы", "quantity": 100.0}
old_pos = {"id": 1, "name": "12W/12-24V/DIN БЛОК ПИТАНИЯ FARADAY", "quantity": 0.0}
try_1 = ["material", 5]

def change_info_pos(data: dict = old_pos):
    try:
        if data_test(data):
            if Positions.objects.filter(id=data["id"]).exists():
                position = Positions(**data)
                position.save()
                print(f"Сохранено в базе: {position.id}, {position.name}, {position.quantity}")
                vvod_info_ch_qant(data, type=5)
            else:
                print(f"Id {data['id']} не найден")
                return HttpResponse("Bad Request: positions.id is absent")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")

change_test_new = ["vvod_info_ch_type", False]


def change_info_ch_type(data: dict = change_test_new):
    try:
        if data_test(data):
            ch_type = Change_types(**data)
            if "name" in data:
                if Change_types.objects.filter(name=data["name"]).exists():
                    old_ch_type = Change_types.objects.get(name=data["name"])
                    old_ch_type = ch_type
                    old_ch_type.save()
                    logging.info("Изменено в базе: %s, %s", old_ch_type.id, old_ch_type.name)
                else:
                    ch_type.save()
                    logging.info("Сохранено в базе: %s, %s", ch_type.id, ch_type.name)
                    vvod_info_ch_qant(data, 11)
            else:
                logging.info("Обязательный атрибут name не определен")
                return HttpResponse("Bad Request: ch_type.name is absent")
        else:
            logging.error("Bad format of data")
            return DataTypeError
    except DataTypeError:
        return HttpResponse("Bad format of data")