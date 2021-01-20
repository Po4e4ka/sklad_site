from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Positions, Persons


def index(request):
    return HttpResponse("")
class PosView(View):
    def get(self, request):
        positions = Positions.objects.all()
        positions = [model_to_dict(position) for position in positions]
        return render(request, "bib_site/books_table.html", context={"positions": positions})