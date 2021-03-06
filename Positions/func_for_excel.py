import os

import openpyxl
import datetime
import random

testData = {
    "dataTime": datetime.date.today(),
    "actNumber": random.randint(0,100000),
    "mol": "Тест Ответтственный",
    "worker": "Тест приемщик",
    "object": "Тест объект",
    "positions": [
        {
            "name":"test1",
            "code":random.randint(0,1000000),
            "ediz":"шт",
            "quantity":random.randint(1,100)
         },
        {
            "name":"test2",
            "code":random.randint(0,1000000),
            "ediz":"шт",
            "quantity":random.randint(1,100)
        }],
    }
path = "prin-template.xlsx"
def write_to_excel(data):

    wb = openpyxl.load_workbook(path)
    xl = wb.active

    datime = xl.cell(3,15)
    ID = xl.cell(3,8)
    mol = xl.cell(6,2)
    prin = xl.cell(9,2)
    obj = xl.cell(12,2)


    datime.value = data["dataTime"]
    ID.value = data["actNumber"]
    mol.value = data["mol"]
    prin.value = data["worker"]
    obj.value = data["object"]

    first = 20
    # first pos


    for i, k in enumerate(data["positions"]):
        first += i
        posID = xl.cell(first, 2)
        posName = xl.cell(first, 4)
        posCode = xl.cell(first, 5)
        posEdiz = xl.cell(first, 7)
        posQuant = xl.cell(first, 12)

        posID.value = i+1
        posName.value = k["name"]
        posCode.value = k["code"]
        posEdiz.value = k["ediz"]
        posQuant.value = k["quantity"]



    if os.path.isfile("1.xlsx"):
        os.remove("1.xlsx")
    wb.save("1.xlsx")

write_to_excel(testData)