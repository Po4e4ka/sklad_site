from django.db.models import Max, Avg
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
    # if 'id' in data:
    #     if Positions.objects.filter(id=data['id']).count() > 0:
    #         return HttpResponse("Bad Request: positions.id is already in base")
    # else:
    #     print()
    #     data['id'] = Positions.objects.all().aggregate(Max('id'))
    #     print(data)
    #     return HttpResponse("OK")
    try:
        position = Positions(**data)

        position.save()
    except:
        return -1
    # return HttpResponse(f"Позиция введена: {position.id}, {position.name}")





