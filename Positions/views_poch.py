import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .func_for_change import change_info_pos, change_info_ch_type, change_test_new, try_1
from .func_for_find import find_pos, find_change
from .func_for_views import vvod_info_ch_type, excel_to_dict, vvod_info_pos, \
    vvod_info_ch_qant, vvod_info_group,\
    vvod_info_xyz, vvod_info_obj, vvod_info_level, vvod_info_person

from .models import Positions, Groups
import sqlite3

#new_pos = {'name': 'БАТАРЕЙКИ LR03 MAX ENERGIZER BB', 'code': '072899', 'quantity': 22, 'ediz': 'шт'}
#xyz_test = {"X": "a", "y": "3"}
#nomenklatura_test = {"name": "сыпучие"}
#level_test = {"name": "test"}
#person_test = {"name": "Дим Димыч", "phone": "777777789"}
#obj_test = {"name": "object10", "adress": "Октябрьская наб. 7"}
#change_test = {"name": "vozvrat", "znak": False}
qant_test = {"position_id": 1, "quantity": "1000.0"}


def index(request):
    #vvod_info_xyz(xyz_test)
    #vvod_info_ch_type(change_test)
    #vvod_info_person(person_test)
    #vvod_info_group(nomenklatura_test)
    #vvod_info_level(level_test)
    #vvod_info_obj(obj_test)
    vvod_info_ch_qant(qant_test, 1)
    #vvod_info_pos(new_pos)

    # change_info_pos(try_1)
     # positions = Positions._meta.get_fields()


    # find_pos('aaa')
    # find_change(datetime.date(2021,3,11), False, 1)

    return HttpResponse('OK')