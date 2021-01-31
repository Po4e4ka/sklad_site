
from django.http import HttpResponse

from Positions.models import Positions

data_test = dict(id=1, code=123456789, name="test", groups_id=1, quantity=10.0, ediz="kg", photo1=None,
                 photo2=None, mol="Ivanov", xyz_id=1)


def vvod_info_pos(data=data_test):
    if type(data) != dict:
        return HttpResponse("Bad Request: wrong type of data")

    # conn = sqlite3.connect("db.sqlite3")
    # cursor = conn.cursor()

    # cursor.execute("""INSERT INTO positions
    #                  VALUES (data)""")

    all_positions = Positions.objects.all()
    if data['id'] not in all_positions.id:
        positions = Positions(
            code=data['code'],
            name=data['name'],
            groups_id=data['groups_id'],
            quantity=data['quantity'],
            ediz=data['ediz'],
            photo1=data['photo1'],
            photo2=data['photo2'],
            mol=data['mol'],
            xyz_id=data[' xyz_id']
        )
        positions.save()
        return HttpResponse(f"введена позиция {positions.id, positions.name}")
    else:
        return HttpResponse("Bad Request: positions.id is already in base")

def test_vvod():
    return HttpResponse("lol_test")