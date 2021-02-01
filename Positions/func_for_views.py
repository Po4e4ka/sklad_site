from django.http import HttpResponse
from Positions.models import Positions


def vvod_info_pos(data: dict):
    if type(data) != dict:
        return HttpResponse("Bad Request: wrong type of data")
    if Positions.objects.filter(id=data['id']).count() < 1:
        position = Positions(**data)
        position.save()
        return HttpResponse(f"Позиция введена: {position.id}, {position.name}")
    else:
        return HttpResponse("Bad Request: positions.id is already in base")

def test_vvod():
    return HttpResponse("lol_test")