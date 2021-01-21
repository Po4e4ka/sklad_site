from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Groups, Xyz, Positions, Levels, Persons, Change_types, Objects, Сhange_qality
from .forms import GroupsModelForm, XyzModelForm, PositionsModelForm, LevelsModelForm, PersonsModelForm, Change_typesModelForm, ObjectsModelForm, Сhange_qalityModelForm



def index(request):
    return HttpResponse("")
class PosView(View):
    def get(self, request):
        positions = Positions.objects.all()
        positions = [model_to_dict(position) for position in positions]
        return render(request, "bib_site/books_table.html", context={"positions": positions})