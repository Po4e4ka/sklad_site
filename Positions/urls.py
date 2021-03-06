from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),  # стартовая страница
    path('new/', views.NewView.as_view(), name="new"),  # новая позиция
    path("list/", views.PositionLisView.as_view(), name="list"),  # таблица позиций
    path("persons/", views.PersonListView.as_view(), name="persons"),  # таблица персон
    path("changes/", views.ChangeListView.as_view(), name="changes"), #таблица изменений
    # path("omagad/", views.bd_func_vvod_start),  # для тестов пост страница
    path("list/position<int:pos_id>/", views.PositionView.as_view(), name="position")  # отображение страницы позиции

]
