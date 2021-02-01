from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# from .func_for_views import vvod_info_pos
from .func_for_views import vvod_info_pos, test_vvod
from .models import Positions
import sqlite3


data_test = {'id' : 1, 'code' : 1, 'name' : "test", 'quantity' : 10.0}


def index(request):
# positions = Positions._meta.get_fields()
# print(positions)
#    return test_vvod() # Это просто проверка, что такой вызов работает из твоего файла
    return HttpResponse(vvod_info_pos(data_test)) # Здесь идет вызов твоей функции
# # return HttpResponse(f'{positions}')

