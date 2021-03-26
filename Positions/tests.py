import json

from django.test import TestCase, Client
from .models import Positions, Groups, Xyz, Levels, Persons, Objects, Change_types, Change_qantity

# Create your tests here.

class PositionsTestCase(TestCase):
    pos1 = {
    "id" : 1,
    "code" : 11111111111,
    "name" : "сверло",
    "quantity" : 10,
    "ediz" : "шт"
    }
    pos2 = {
        "id": 2,
        "code": 22222222222,
        "name": "камера",
        "quantity": 50,
        "ediz": "шт"
    }

    def setUp(self):
        pos1 = Positions.objects.create(**self.pos1)
        pos2 = Positions.objects.create(**self.pos2)

    def test_pos_list(self):
        client = Client()
        response = client.get('/position/')
        self.assertEqual(response.status_code, 200)

        data = response.json() # json.loads(response.body)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], self.pos1)
        self.assertEqual(data[1], self.pos2)

    def test_pos_get(self):
        client = Client()
        response = client.get('/position/2')

        self.assertEqual(response.status_code, 200)
        data = response.json() # json.loads(response.body)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['id'], 2)
        self.assertEqual(data['name'], 'камера')
        self.assertEqual(data['quantity'], 50)
        self.assertEqual(data['code'], 11111111111)

    def test_pos_not_exist(self):
        client = Client()
        response = client.get('/position/42')
        self.assertEqual(response.status_code, 404)

    def test_pos_delete(self):
        client = Client()
        response = client.delete('/position/2')
        self.assertEqual(response.status_code, 204)
        response = client.get('/position/2')
        self.assertEqual(response.status_code, 404)

    # def test_book_create(self):
    #     test_book = {"name" : "book3",
    #     "author_name" : "author3",
    #     "pablish_date" : "2003-03-03"}
    #
    #     client = Client()
    #     response = client.post('/books/',
    #                 json.dumps(test_book),
    #                 content_type="application/json")
    #     self.assertEqual(response.status_code, 201)
    #
    #     self.assertIsInstance(response.json(), dict)
#        self.assertEqual(response["name"], 'book3')
