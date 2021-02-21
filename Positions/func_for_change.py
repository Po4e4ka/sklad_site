from .func_for_views import data_test, vvod_info_ch_qant
from django.http import HttpResponse
from .models import Positions, Change_types



new_pos = {"id": 1, "name": "материалы", "quantity" : 100.0}
old_pos = {"id": 1, "name": "12W/12-24V/DIN БЛОК ПИТАНИЯ FARADAY", "quantity" : 0.0}

def change_info_pos(data: dict = old_pos):
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
            ]


def change_info_ch_type(data: dict = change_test_new):
    data_test(data)
    if Change_types.objects.filter(name=data["name"]).exists():
        ch_type = Change_types(**data)
        ch_type.save()
        print(f"Сохранено в базе: {ch_type.id}, {ch_type.name}, {ch_type.znak}")
        vvod_info_ch_qant(data, type=11)
    else:
        print(f"Id {data['name']} не найден")
        return HttpResponse("Bad Request: ch_type.id is absent")