from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Positions



def index(request):
    positions = Positions._meta.get_fields()
    print(positions)
    return HttpResponse(f'{positions}')

class NewView(View):
    def get(self, request):
        return render(request, 'Positions/new_position.html')

    def post(self, request):
        pass