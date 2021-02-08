from .func_for_views import data_test
from django.http import HttpResponse
from .models import Positions


new_pos = {"id": 1, "name": "материалы", "quantity" : 100.0}
old_pos = {"id": 1, "name": "12W/12-24V/DIN БЛОК ПИТАНИЯ FARADAY", "quantity" : 0.0}

def change_info_pos(data: dict = old_pos):
    data_test(data)
    if Positions.objects.filter(id=data["id"]).count() > 0:
#        position = Positions.objects.filter(id=data["id"])
        position = Positions(**data)
        position.save()
        print(f"Сохранено в базе: {position.id}, {position.name}, {position.quantity}")
    else:
        print(f"Id {data['id']} не найден")
        return HttpResponse("Bad Request: positions.id is absent")