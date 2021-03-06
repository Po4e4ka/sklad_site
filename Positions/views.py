from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Positions, Persons, Change_qantity


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
        for key, item in main_dict.items():
            html += f"{key}: {item}<br>"
        html += '<input type="button" onclick="history.back();" value="Назад"/></body></html>'
        return HttpResponse(html)
# Таблица позиций
class PositionLisView(View):
    """Вид и пост списка всех позиций"""
    def get(self, request, sort='id'):
        print(request,sort)
        positions = Positions.objects.order_by(sort, "id")
        return render(request, "Positions/Tables/positions_view_table.html", context={"positions":positions})
    def post(self, request):
        pass
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
    def get(self):
        pass
    def post(self):
        pass


