from .models import Groups, Xyz, Positions, Levels, Persons, Change_types, Objects, Change_qantity
from django.http import HttpResponse


def vvod_info_pos(data: dict):
    if type(data) != dict:
        return HttpResponse("Bad Request: wrong type of data")
    if len(data) != 10:
        return HttpResponse("Bad Request: information is not enough ")
    positions = Positions(**data)
    all_positions = Positions.objects.all()
    if positions.id not in all_positions:
        positions.save()
        return HttpResponse(f"введена позиция {positions.id, positions.name}")
    else:
        return HttpResponse("Bad Request: positions.id is already in base")


