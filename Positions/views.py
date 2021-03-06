from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .func_for_views import vvod_info_pos
from .func_for_find import find_pos
from .models import Positions, Persons, Change_qantity, Objects

import re

out_dict = {"positions":[]}

# Начальная страница
def index(request):
    return render(request, 'Positions/home_menu.html')
# Добавление позиции
class NewView(View):
    """Вид и пост странички новой позиции"""
    def get(self, request):
        persons = Persons.objects.filter(level_id="3")
        return render(request, 'Positions/new_position.html', context={"persons": persons})

    def post(self, request):
        # реобразование в словарь всех данных из пост
        main_dict = dict(request.POST.items())
        html = "<html><body>Успешно добавлено<br>"

        del main_dict["csrfmiddlewaretoken"]
        del main_dict["image1"]
        del main_dict["image2"]
        main_dict["code"] = int(main_dict["code"])
        main_dict["quantity"] = int(main_dict["quantity"])
        main_dict["mol"] = int(main_dict["mol"])
        print(main_dict)
        vvod_info_pos(main_dict)

        for key, item in main_dict.items():
            html += f"{key}: {item}<br>"
        html += '<input type="button" onclick="history.back();" value="Назад"/></body></html>'

        return HttpResponse(html)
# Таблица позиций
class PositionLisView(View):
    """Вид и пост списка всех позиций"""
    def get(self, request):
        check = request.GET.get("null") == '1'
        if check:
            positions = Positions.objects.all()
        else:
            positions = Positions.objects.exclude(quantity=0).exclude(quantity=None)
        return render(request, "Positions/Tables/positions_view_table.html", context={"positions":positions, "check":check})
    def post(self, request):

        _dict = dict(request.POST.items())
        print(_dict["reg_search"])
        if _dict["reg_search"] is not None:
            positions = find_pos(_dict["reg_search"])
        else:
            positions = Positions.objects.all()
        check = request.GET.get("null") == '1'
        if not check:
            positions = positions.exclude(quantity=0).exclude(quantity=None)
        return render(request, "Positions/Tables/positions_view_table.html",
                      context={"positions": positions, "check": check})


# Позиция
class PositionView(View):
    def get(self, request, pos_id):
        pos = Positions.objects.get(pk=pos_id)
        return render(request, "Positions/position_view.html", context={"position":pos})
    def post(self, request):
        pass
# Таблица работнков
class PersonListView(View):
    def get(self, request):
        persons = Persons.objects.all()
        return render(request, "Positions/Tables/Persons_view_table.html", context={"persons":persons})
    def post(self):
        pass
# Работник
class PersonView(View):
    def get(self):
        pass
    def post(self):
        pass
# Таблица изменений
class ChangeListView(View):
    def get(self, request):
        changes = Change_qantity.objects.all()
        return render(request, "Positions/Tables/change_view_table.html", context={"changes":changes})
    def post(self):
        pass
# Изменение
class ChangeView(View):
    def get(self, request):

        if request.GET.get("list") is not None:
            out_dict["positions"].append(Positions.objects.get(pk=request.GET.get("list")))

        persons = Persons.objects.filter(level_id="3")
        arb = Persons.objects.all()
        objects = Objects.objects.all()
        positions = Positions.objects.exclude(quantity=0).exclude(quantity=None)
        if request.GET.get("reg_search") is not None:
            return render(request, "Positions/Tables/pos_select.html", context={"positions":positions})

        return render(request, "Positions/change_out.html",
                      context={
                          "persons":persons,
                          "arb":arb,
                          "objects":objects,
                          "positions": positions,
                          "out_dict": out_dict,
                          "pos": out_dict["positions"]
                      })
    def post(self, request):
        positions = Positions.objects.exclude(quantity=0).exclude(quantity=None)
        _dict = dict(request.POST.items())
        out_dict["mol"] = Persons.objects.get(pk=_dict["mol"]) if _dict["mol"] != '' else None
        out_dict["arb"] = Persons.objects.get(pk=_dict["arb"]) if _dict["arb"] != '' else None
        out_dict["obj"] = Objects.objects.get(pk=_dict["obj"]) if _dict["obj"] != '' else None
        return render(request, "Positions/Tables/pos_select.html", context={"positions":positions})





class ObectsView(View):
    def get(self, request):
        _objects = Objects.objects.all()
        return render(request, "Positions/Tables/objects_table.html", context={"objects":_objects})


