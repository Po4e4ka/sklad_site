from django.http import HttpResponse
from .models import Positions, Groups, Xyz, Levels, Persons, Objects, Change_types, Change_qantity
from datetime import datetime
import logging

# filemode="w"
logging.basicConfig(filename="sample.log", format='[%(asctime)s] [%(levelname)s] => %(message)s', level=logging.INFO)



# def find_pos(data: str = False, code_pos: int = False):
def find_pos(data: str = False, code_pos: int = False):
    try:
        if data and not code_pos:
            if Positions.objects.filter(name__icontains=data):
                logging.info("Выбрано %s позиций", len(Positions.objects.filter(name__icontains=data)))
                return Positions.objects.filter(name__icontains=data)
            else:
                logging.info("По запросу %s позиций не найдено", str)
        if not data and code_pos:
            if Positions.objects.filter(code__icontains=code_pos):
                logging.info("Выбрано %s позиций", len(Positions.objects.filter(code__icontains=code_pos)))
                return Positions.objects.filter(code__icontains=code_pos)
            else:
                logging.info("По запросу %s позиций не найдено", code_pos)
        if data and code_pos:
            if Positions.objects.filter(code__icontains=code_pos):
                logging.info("Выбрано %s позиций", len(Positions.objects.filter(code__icontains=code_pos).filter(name__icontains=data)))
                return Positions.objects.filter(code__icontains=code_pos).filter(name__icontains=data)
            else:
                logging.info("По запросу %s и %ы позиций не найдено", data, code_pos)
    except Exception as e:
        logging.error("Request parameters is not defined, %s", e)
        return HttpResponse("Bad Request: Parameters is not defined")




