# from django.db.models import Max, Avg
from django.http import HttpResponse
from Positions.models import Positions
import pandas as pd


def excel_to_dict(file="Positions/Копия 1.xls"):
    # Load spreadsheet
    xl = pd.ExcelFile(file)
    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse('номенклатура')
    result = []
    for index, row in df1.iterrows():
        if type(row['номенклатура']) == float:
            break
        result.append({"name":row['номенклатура'],"quantity":row["количество"], "ediz":row["ед.измер."]})
    return result


def vvod_info_pos(data: dict):
    print(data)
    if type(data) != dict:
        return HttpResponse("Bad Request: wrong type of data")
    if 'name' in data:
        if Positions.objects.filter(name=data['name']).count() > 0:
            return HttpResponse("Bad Request: positions.id is already in base")
            """
            подумать насчет действий, если необходимо внести свежие данные о наличии при загрузке 
            из внешних источников, а позиция уже есть в БД:
            1. Обновляем данные или оставляем старые
            2. Куда записывается информация:
             - о конфликте (в том числе по каким графам есть отклонения);
             - об удаляемых данных;
             - предлагается ли ручная корректировка
            """
    else:
        try:
            position = Positions(**data)
            position.save()
        except:
            return -1

#     data['id'] = Positions.objects.all().aggregate(Max('id'))
#     print(data)
#     return HttpResponse("OK")

# return HttpResponse(f"Позиция введена: {position.id}, {position.name}")





