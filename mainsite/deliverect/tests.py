from django.test import TestCase
from termcolor import colored
from .models import (Menu,
                    Order)

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
import copy



class TestDeliverectApp(TestCase):
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
            self.assertEqual(Menu.objects.get(uuid=test['pk']).price, single_unit_test['price'])
            self.assertEqual(Menu.objects.get(uuid=test['pk']).quantity, single_unit_test['quantity'])
            self.assertEqual(type(Menu.objects.get(uuid=test['pk'])), Menu)
            self.assertEqual(type(ModelSerializer(Menu.objects.get(uuid=test['pk'])).data), ReturnDict)
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
        self.assertEqual(type(Menu.objects.all()[0].pk), uuid.UUID)
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
        self.assertRaises(Exception, Menu.objects.get, pk=f'{uuid.uuid4()}') #random Object


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



    def test_bad_end_points_orders(self)-> None:
        print(colored('Testing endpoints orders methods \U0001F4C3', 'green'))
        data = {
            'description': "description product 1",
            'price': 12.3,
            'quantity':300
        }



        url=reverse('order_handler')
        self.assertEqual(self.client.post(url).status_code, 400) #empty request
        self.assertEqual(self.client.get(url).status_code, 404) #empty request
        self.assertEqual(self.client.put(url).status_code, 405)
        self.assertEqual(self.client.patch(url).status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 405)
        self.assertEqual(self.client.options(url).status_code, 405)
        self.assertEqual(self.client.post(url,data=data).status_code, 400) #invalid data

        data={
            'order':[
                {
                    'uuid':f'{uuid.uuid4()}',
                    "quantity":23
                },
                {
                    'uuid':f'{uuid.uuid4()}',
                    'quantity':23
                }
            ],
            'info':{
                'note':"bla bla",
                'payment':286.8
            }
            }

        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        self.assertEqual(resp.headers['Content-Type'],'application/json')
        self.assertEqual(resp.json()['status'], 'error')
        self.assertEqual(resp.json()['data']['msg'], 'uuid not found')

        d=copy.deepcopy(data) #remove part of the body
        del(d['info'])
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        d=copy.deepcopy(data) #remove part of the body
        del(d['order'])
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        d=copy.deepcopy(data) #remove part of the body
        d['order']=[]
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        d=copy.deepcopy(data) #remove part of the body
        del(d['info']['payment'])
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        d=copy.deepcopy(data) #remove part of the body
        del(d['info']['note'])
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        d=copy.deepcopy(data) #remove part of the body
        d['info']['payment']=-23 #negative payment
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        d=copy.deepcopy(data) #remove part of the body
        d['info']['payment']=True #negative payment
        resp=self.client.post(url, data=d, content_type='application/json')
        self.assertEqual(resp.status_code, 400) #invalid data
        self.assertEqual(resp.json()['error'], 'bad json schema')



    def test_end_points_orders(self)-> None:
        print(colored('Testing another endpoints orders methods \U0001F4C3', 'green'))

        test_case_1=self.test_cases[random.randint(0,len(self.test_cases)-1)]
        test_case_2=self.test_cases[random.randint(0,len(self.test_cases)-1)]


        data = {

            'order':[
                {
                    'uuid':test_case_1['pk'],
                    'quantity':1
                },
                {
                    'uuid':test_case_2['pk'],
                    'quantity':1
                }
            ],
            'info':{
                'note':'bla bla',
                'payment':0,
            }
        }


        url=reverse('order_handler')
        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['status'], 'error')
        self.assertEqual(resp.json()['data']['msg'], 'payment is not correct')

        data['order'][0]['quantity']=test_case_1['fields']['quantity']+1 #too much quantity for the product
        data['order'][1]['quantity']=test_case_1['fields']['quantity']+1 #too much quantity for the product
        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['status'], 'error')
        self.assertEqual(resp.json()['data']['msg'], 'quantity not available')

        #build correct inputs for the test
        test_case_1=self.test_cases[random.randint(0,len(self.test_cases)-1)]
        test_case_2=self.test_cases[random.randint(0,len(self.test_cases)-1)]


        order_1=2
        order_2=3
        total=round(test_case_1['fields']['price']*order_1+test_case_2['fields']['price']*order_2,2)
        data = {

            'order':[
                {
                    'uuid':test_case_1['pk'],
                    'quantity':order_1
                },
                {
                    'uuid':test_case_2['pk'],
                    'quantity':order_2
                }
            ],
            'info':{
                'note':'bla bla',
                'payment':total
            }
        }

        resp=self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['status'], 'success')
        uuid=resp.json()['uuid']

        resp=self.client.get(url+'/'+uuid, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len({test_case_1['pk'],test_case_2['pk']}.difference({i['menu'] for i in resp.json()['order']['items']})),0)






    def test_database_orders(self)-> None:
        print(colored('Testing database orders \U0001F4C3', 'green'))
        order=Order()
        order.save()
        self.assertEqual(type(order.uuid), uuid.UUID)
        self.assertEqual(type(order.created_at), datetime)
        self.assertEqual(type(order.note), str)
        self.assertEqual(type(order.amount), float)
        self.assertEqual(Order.objects.all().count(), 1)
        #delete object
        self.assertEqual(Order.objects.all().delete()[0],1)
        self.assertEqual(Order.objects.all().delete()[0],0)
        self.assertEqual(Order.objects.all().count(), 0)
        order=Order(amount=12.3, note="bla bla")
        order.save()
        self.assertEqual(type(order.uuid), uuid.UUID)
        self.assertEqual(order.amount, 12.3)
        self.assertEqual(order.note, "bla bla")
        self.assertEqual(Order.objects.all().count(), 1)
        order.note='updated note'
        order.save()
        self.assertEqual(Order.objects.all().count(), 1)#single object
        self.assertEqual(Order.objects.all()[0].note, 'updated note')





    def tearDown(self) -> None:
        print(colored('Dropping testing database \U0001F4A3 ', 'green'))
