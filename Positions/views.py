from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# from .func_for_views import vvod_info_pos
from .models import Positions
import sqlite3



def index(request):
    positions = Positions._meta.get_fields()
    print(positions)
    return HttpResponse(f'{positions}')



