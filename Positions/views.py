from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Positions, Persons

from .func_for_views import excel_to_dict, vvod_info_pos, vvod_info_group, nomenklatura_test, \
    xyz_test, vvod_info_xyz, obj_test, vvod_info_obj,\
    level_test, vvod_info_level, vvod_info_person, person_test



def index(request):
    return render(request, 'Positions/home_menu.html')

class NewView(View):
    """Вид и пост странички новой позиции"""
    def get(self, request):
        persons = Persons.objects.filter(level_id="3")
        return render(request, 'Positions/new_position.html', context={"persons": persons})

    def post(self, request):
        # реобразование в словарь всех данных из пост
        main_dict = dict(request.POST.items())
        # Создание нового автора, если такого нет в таблице Авторы или сслыка на существующую запись
        # author = Author.objects.get_or_create(name=main_dict['author'])
        # if isinstance(author, tuple):
        #     author = author[0]
        # Создание новой книги с информацией, полученной из формы
        # book = Book.objects.create(name=main_dict['name'],
        #                            publishDate=main_dict['publishDate'],
        #                            genre=main_dict['genre'],
        #                            author_id=author)
        # book.save()
        html = "<html><body>Успешно добавлено<br>"
        for key, item in main_dict.items():
            html += f"{key}: {item}<br>"
        html += '<input type="button" onclick="history.back();" value="Назад"/></body></html>'
        return HttpResponse(html)

class PositionLisView(View):
    """Вид и пост списка всех позиций"""
    def get(self, request, sort='id'):
        print(request,sort)
        positions = Positions.objects.order_by(sort, "id")
        return render(request, "Positions/positions_view_table.html", context={"positions":positions})
    def post(self, request):
        pass

def bd_func_vvod_start(request):
    """Функция заноса тестовых значений из таблицы"""
    for i in excel_to_dict():
        vvod_info_pos(i)
    for i in nomenklatura_test:
        vvod_info_group(i)
    #    for i in xyz_test:
    #        vvod_info_xyz(i)
    for i in level_test:
        vvod_info_level(i)
    for i in person_test:
        vvod_info_person(i)
    for i in obj_test:
        vvod_info_obj(i)
    return HttpResponse('OK')

class PositionView(View):
    def get(self, request, pos_id):
        pos = Positions.objects.get(pk=pos_id)
        return render(request, "Positions/position_view.html", context={"position":pos})
    def post(self, request):
        pass