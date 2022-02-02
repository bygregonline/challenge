from django.test import TestCase
from termcolor import colored
from .models import Menu
from .utils import is_valid_uuid

from .serializers import ModelSerializer
import json
import uuid
from rest_framework.utils.serializer_helpers import ReturnDict
from pathlib import Path
from datetime import datetime
from django.db.utils import IntegrityError
from django.db import transaction
from django.urls import reverse
from django.core.exceptions import ValidationError
import random



class TestDatabase(TestCase):
    fixtures = ["data.json"]

    def setUp(self) -> None:
        print(colored('Build database from fixtures database \U0001F448', 'green'))
        test_cases_file = Path(__file__).resolve().parent / 'fixtures' / 'data.json'
        with open(test_cases_file, 'r') as f:
            self.test_cases = json.load(f)
        print(colored(f'Reading {len(self.test_cases)} test cases from {test_cases_file} \U0001F448', 'green'))
        self.data ={'description':'Pizza with  some extra ingredients', 'price':24.45, 'quantity':400}






    def test_database(self) -> None:
        print(colored('Testing database methods \U0001F4C3', 'green'))
        self.assertTrue(True) #just a flag test
        self.assertEqual(Menu.objects.count(), len(self.test_cases))

        for test in self.test_cases:
            single_unit_test =test['fields']
            self.assertEqual(Menu.objects.get(id=test['pk']).description,single_unit_test['description'])
            self.assertEqual(Menu.objects.get(uuid=single_unit_test['uuid']).price, single_unit_test['price'])
            self.assertEqual(Menu.objects.get(uuid=single_unit_test['uuid']).quantity, single_unit_test['quantity'])
            self.assertEqual(type(Menu.objects.get(uuid=single_unit_test['uuid'])), Menu)
            self.assertEqual(type(ModelSerializer(Menu.objects.get(uuid=single_unit_test['uuid'])).data), ReturnDict)
            self.assertEqual(Menu.objects.get(id=test['pk']).price, single_unit_test['price'])
        #another basic database  test
        self.assertEqual(Menu.objects.all().delete()[0],len(self.test_cases))
        self.assertEqual(Menu.objects.all().delete()[0],0)
        self.assertEqual(Menu.objects.all().count(), 0)
        self.assertEqual(Menu(**self.data).save(),None)
        self.assertEqual(Menu.objects.all().count(), 1)
        #test types
        self.assertEqual(type(Menu.objects.all()[0].uuid), uuid.UUID)
        self.assertEqual(type(Menu.objects.all()[0].description), str)
        self.assertEqual(type(Menu.objects.all()[0].price), float)
        self.assertEqual(type(Menu.objects.all()[0].quantity), int)
        self.assertEqual(type(Menu.objects.all()[0].pk), int)
        self.assertEqual(type(Menu.objects.all()[0].__dict__), dict)
        self.assertEqual(type(Menu.objects.all()[0].created_at), datetime)
        self.assertEqual(Menu.objects.all().delete()[0],1)
        self.assertEqual(Menu.objects.all().count(), 0)
        #test default values
        self.assertEqual(Menu().save(),None) #default values "are or must" be set
        self.assertNotEqual(Menu.objects.all().count(), 0)
        self.assertNotEqual(Menu.objects.all()[0].quantity, None)
        self.assertNotEqual(Menu.objects.all()[0].description, None)
        self.assertNotEqual(Menu.objects.all()[0].price, None)
        self.assertNotEqual(Menu.objects.all()[0].uuid, None)
        self.assertNotEqual(Menu.objects.all()[0].created_at, None)
        self.assertEqual(Menu.objects.all().delete()[0],1)

        self.assertEqual(Menu.objects.all().count(), 0)

        self.assertRaises(Exception, Menu.objects.get, uuid=f'{uuid.uuid4()}') #random Object


        # print(.deliverect.models.Menu.DoesNotExist)



    def test_database_constraints(self) -> None:
        print(colored('Testing database constraints \U0001F4C3', 'green'))
        try:
            with transaction.atomic():
                Menu.objects.create(name="")
        except Exception as e:
            self.assertEqual(TypeError, type(e))
        try:
            with transaction.atomic():
                Menu.objects.create(description=None)
        except Exception as e:
            self.assertEqual(IntegrityError, type(e))
        try:
            with transaction.atomic():
                Menu.objects.create(quantity=None)
        except Exception as e:
            self.assertEqual(ValidationError, type(e))
        try:
            with transaction.atomic():
                Menu.objects.create(price=None)
        except Exception as e:
            self.assertEqual(ValidationError, type(e))





    def test_end_points(self)-> None:
        print(colored('Testing end points \U0001F4C3', 'green'))
        self.assertTrue(True) #just a test to see if the app is working
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 404)
        url=reverse('menu_handler')
        resp = self.client.get(url)
        #retrieve all
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.json()), list)
        self.assertEqual(len(resp.json()), len(self.test_cases))
        #get single menu
        data = resp.json()
        single_test=data[random.randint(0,len(data))-1]

        resp = self.client.get(url+'/'+single_test['uuid'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.json()), dict)


        #invalid data
        data = {
            'name': 'name',
        }
        self.assertEqual(self.client.post(url, data=data, content_type='application/json').status_code, 400)
        #invalid rest methods
        self.assertEqual(self.client.put(url, data=data, content_type='application/json').status_code, 405)
        self.assertEqual(self.client.options(url, data=data, content_type='application/json').status_code, 405)
        data = {
            'description': "description product 1",
            'price': 12.3,
            'quantity':300
        }
        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['status'], 'ok')
        self.assertEqual(is_valid_uuid((resp.json()['uuid'])) , True)
        self.assertEqual(resp.headers['Content-Type'],'application/json')
        data = {
            'description': "description product 1",
            'price': "asdsds",
            'quantity':300
        }
        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers['Content-Type'],'application/json')
        data = {
            'description': "description product 1",
            'price': "300",
            'quantity':"sadssdd"
        }
        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers['Content-Type'],'application/json')
        data = {
            'description': 34.5,
            'price': "300",
            'quantity':"sadssdd"
        }
        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers['Content-Type'],'application/json')

        #delete all one by one
        resp = self.client.get(url)

        for single_test in resp.json():
            resp1 = self.client.delete(url+'/'+single_test['uuid'])
            self.assertEqual(resp1.status_code, 200)
            self.assertEqual(resp1.headers['Content-Type'],'application/json')
            self.assertEqual(resp1.json()['status'],'success')

        resp =self.client.delete(url) #delete without UUID
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers['Content-Type'],'application/json')
        #after delete all menues
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 0)

        #create new one for testing patch
        resp=self.client.post(url, data=self.data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['status'], 'ok')
        self.assertEqual(is_valid_uuid((resp.json()['uuid'])) , True)
        single_uuid=resp.json()['uuid'] #new uuid has been created


        resp=self.client.patch(url, data=self.data, content_type='application/json') #patch without uuid
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.headers['Content-Type'],'application/json')

        resp=self.client.patch(url+'/'+single_uuid, data={'price':34.2}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.json()), dict)
        self.assertEqual(resp.json()['status'], 'success')
        self.assertEqual(resp.json()['data']['price'], 34.2)
        self.assertEqual(resp.json()['data']['quantity'], 400)

        resp=self.client.patch(url+'/'+single_uuid, data={'quantity':804.2}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.json()), dict)
        self.assertEqual(resp.json()['status'], 'error')

        resp=self.client.patch(url+'/'+single_uuid, data={'price':"SADSDF.2"}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(type(resp.json()), dict)
        self.assertEqual(resp.json()['status'], 'error')


        resp=self.client.patch(url+'/'+single_uuid, data={'algo':"SADSDF.2"}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(type(resp.json()), dict)


        #testing testing pages
        self.assertEqual(self.client.get(reverse('testing-error')).status_code, 500)

        resp = self.client.get(reverse('get_process'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['Content-Type'],'text/plain')

        resp = self.client.get(reverse('get_info'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['Content-Type'],'application/json')
        self.assertEqual(type(resp.json()), dict)








    def tearDown(self) -> None:
        print(colored('Dropping testing database \U0001F4A3 ', 'green'))
