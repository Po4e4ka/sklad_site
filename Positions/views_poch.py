import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .func_for_change import change_info_pos, change_info_ch_type, change_test_new, try_1
from .func_for_find import find_pos, find_change
from .func_for_views import vvod_info_ch_type, change_test, excel_to_dict, vvod_info_pos, \
    vvod_info_ch_qant, vvod_info_group, nomenklatura_test, \
    xyz_test, vvod_info_xyz, obj_test, vvod_info_obj, \
    level_test, vvod_info_level, vvod_info_person, person_test, qant_test

from .models import Positions, Groups
import sqlite3



def index(request):
    # for i in change_test:
    #     vvod_info_ch_type(i)
    # for i in person_test:
    #     vvod_info_person(i)
    # for i in nomenklatura_test:
    #     vvod_info_group(i)
    # for i in xyz_test:
    #     vvod_info_xyz(i)
    # for i in level_test:
    #     vvod_info_level(i)
    # for i in obj_test:
    #     vvod_info_obj(i)
    # vvod_info_pos(qant_test, 1)

    # change_info_pos(try_1)
     # positions = Positions._meta.get_fields()
    # vvod_info_ch_qant(qant_test, 1)
    # change_info_ch_type(change_test_new)
    # find_pos('камера')
    # find_change(datetime.date(2021,3,11), False, 1)

    return HttpResponse('OK')