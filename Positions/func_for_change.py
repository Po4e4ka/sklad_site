from .func_for_views import vvod_info_ch_qant, data_test
from django.http import HttpResponse
from .models import Positions, Change_types
import logging


logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)


new_pos = {"id": 1, "name": "материалы", "quantity": 100.0}
old_pos = {"id": 1, "name": "12W/12-24V/DIN БЛОК ПИТАНИЯ FARADAY", "quantity": 0.0}

def change_info_pos(data: dict = new_pos):
    data_test(data)
    if Positions.objects.filter(id=data["id"]).exists():
#        position = Positions.objects.filter(id=data["id"])
        position = Positions(**data)

        position.save()
        print(f"Сохранено в базе: {position.id}, {position.name}, {position.quantity}")
        vvod_info_ch_qant(data, type=5)
    else:
        print(f"Id {data['id']} не найден")
        return HttpResponse("Bad Request: positions.id is absent")


change_test_new = [
             {"id": 1, "name": "prihod", "znak": False},
             {"id": 2, "name": "rashod", "znak": True},
             {"id": 3, "name": "izlishki", "znak": False},
             {"id": 4, "name": "nedostacha", "znak": True},
             {"id": 5, "name": "vvod_info_pos"},
             {"id": 6, "name": "vvod_info_group"},
             {"id": 7, "name": "vvod_info_xyz"},
             {"id": 8, "name": "vvod_info_level"},
             {"id": 9, "name": "vvod_info_person"},
             {"id": 10, "name": "vvod_info_obj"},
             {"id": 11, "name": "vvod_info_ch_type"}
            ]


def change_info_ch_type(data: dict = change_test_new):
    data_test(data)
    try:
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
    except Exception as e:
        logging.error("Change_type is not saved %s", e)
        return HttpResponse("Bad Request: ch_type is not saved")