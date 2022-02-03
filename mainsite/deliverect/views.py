
from django.http import Http404, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from pyvalid import accepts, returns
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
import platform
import logging
from .utils import validate_form,validate_schema
from .models import (Menu,
                    Order,
                    OrderItem)
from .serializers import (ModelSerializer,
                          OrderSerializer,
                          OrderItemSerializer)
from datetime import datetime
import subprocess
import traceback
from .schemas import orders_schema
from django.db import transaction




# Create your views here.

@require_http_methods(['GET'])
@returns(JsonResponse)
def get_info(req: WSGIRequest) -> JsonResponse:
    """AI is creating summary for get_info

    Args:
        req (WSGIRequest): [description]

    Returns:
        JsonResponse: [description]
        Just for testing purpose
    """

    d={'version':0.01,'os':platform.system(),'version':platform.version(),'release':platform.release(),'machine':platform.machine(),'processor':platform.processor(),'python_version':platform.python_version()}
    return JsonResponse(d, safe=False)


#
#
@require_http_methods(['GET'])
@accepts(WSGIRequest)
@returns(HttpResponse)
def get_process(req: WSGIRequest)->HttpResponse: #to see whats appends in the container
    command = "ps -Af"
    sub = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    subprocess_return = sub.stdout.read().decode('utf-8')
    return HttpResponse(subprocess_return, status=200,content_type='text/plain')



#


#
@csrf_exempt
@require_http_methods(["PATCH","POST","DELETE","GET"])
@accepts(WSGIRequest)
@returns(JsonResponse,HttpResponse)
def menu_handler(req: WSGIRequest,uuid=None):


    try:
        if req.method == 'PATCH':
            return menu_handler_patch(req,uuid=uuid)
        elif req.method == 'POST':
            return menu_handler_post(req)
        elif req.method == 'GET':
            return  menu_handler_get(req,uuid=uuid)
        elif req.method == 'DELETE':
            return menu_handler_delete(req,uuid=uuid)

    except Exception as e:
        #logging.error(e)

        return JsonResponse({'error':str(e)}, status=400)




@validate_form()
@require_http_methods(['GET'])
def menu_handler_get(req: WSGIRequest,data=None,uuid=None):
    if uuid: #one sigle object request
        obj = Menu.objects.all().filter(uuid=uuid)
        if not obj:
            return JsonResponse({'UUID':uuid,'status':'Not found'}, status=404)
        else:
            return JsonResponse(ModelSerializer(obj[0]).data, safe=False, status=200)
    return JsonResponse(ModelSerializer(Menu.objects.all(), many=True).data, safe=False)







# @validate_form(keys={'description','price','quantity'})
@returns(JsonResponse,HttpResponse)
@validate_form(keys={'description','price','quantity'},partial=True)
def menu_handler_patch(req: WSGIRequest,data=None,uuid=None):
    if not uuid:
        return JsonResponse({'status':'error','message':'UUID is required','time':str(datetime.now()) },status=400)
    obj = Menu.objects.all().filter(uuid=uuid)
    if not obj:
        return JsonResponse({'UUID':uuid,'status':'Not found'}, status=404)
    else:
        menu_serializer = ModelSerializer(obj[0], data=data, partial=True)
        if menu_serializer.is_valid(): #simple validation before saving
            menu_serializer.save()
            return JsonResponse({"status": "success", "data": menu_serializer.data})
        else:
            return JsonResponse({"status": "error", "data": menu_serializer.errors})










@validate_form(keys={'description','price','quantity'})
@returns(JsonResponse,HttpResponse)
def menu_handler_post(req: WSGIRequest,data=None):
    try:
        menu=Menu(**data)
        menu.save()
        return  JsonResponse({'status':'ok','uuid':menu.uuid,'time':str(datetime.now()) },status=201)
    except Exception as e:
        return JsonResponse({'error':'todo'}, status=400)







@validate_form()
@returns(JsonResponse)
def menu_handler_delete(req: WSGIRequest,uuid=None):
    if not uuid:
        return JsonResponse({'status':'error','message':'UUID is required','time':str(datetime.now()) },status=400)
    else:
        obj = Menu.objects.all().filter(uuid=uuid)
        if not obj:
            return JsonResponse({'UUID':uuid,'status':'Not found'}, status=404)
        else:
            obj.delete()
            return JsonResponse({'status':'success','time':str(datetime.now()), 'data':f'item {uuid} has been deleted' },status=200)




@require_http_methods(['GET'])
def testing_error(req: WSGIRequest):
    return HttpResponse(status=500)



@csrf_exempt
@require_http_methods(["POST","GET"])
@accepts(WSGIRequest)
@returns(JsonResponse,HttpResponse)
def order_handler(req: WSGIRequest,uuid=None):
    try:
        if req.method == 'GET':
            return order_handler_get(req,uuid=uuid)
        elif req.method == 'POST':
            return order_handler_post(req)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=400)





@validate_form(keys={'order','info'})
@validate_schema(schema=orders_schema)
@returns(JsonResponse,HttpResponse)
def order_handler_post(req: WSGIRequest,data=None):
    print('\n\n\ninit request')
    orders = data['order']
    info = data['info']
    #print(data)

    reduced_orders=dict()
    try:
        for order in orders: #reducing the orders to one if multiple orders are sent with the same id
            if order['uuid'] in reduced_orders:
                reduced_orders[order['uuid']] += order['quantity']
            else:
                reduced_orders[order['uuid']] = order['quantity']
        #read data from db
        data_from_db=[data for data in Menu.objects.filter(uuid__in=reduced_orders.keys())]
        #validate data if uuid orders does not exist
        differences= (set(reduced_orders.keys() ).difference(set([str(data.uuid) for data in data_from_db])))
        if differences:
            return JsonResponse({'status':'error','data':{'msg':f'uuid not found','invalid':f'{differences}'},'time':str(datetime.now())}, status=400)
        #validate data if quantity is available
        invalid_quantities=[]
        for menu in data_from_db:
            if menu.quantity < reduced_orders[str(menu.uuid)]:
                invalid_quantities.append(str(menu.uuid))
        if invalid_quantities:
            return JsonResponse({'status':'error','data':{'msg':f'quantity not available','invalid':f'{invalid_quantities}'},'time':str(datetime.now())}, status=400)

        #validate  if payment is correct
        ammoun_to_be_paid=round(sum([reduced_orders[str(data.uuid)]*data.price for data in data_from_db if str(data.uuid) in reduced_orders]),2)  #O(n) only one loop for all keys in the dict
        if abs(ammoun_to_be_paid-info['payment']) > 0.01: #one cent gap
            return JsonResponse({'status':'error','data':{'msg':f'payment is not correct','invalid':f"{ammoun_to_be_paid} != {info['payment']} "},'time':str(datetime.now())}, status=400)

        #save order all ok
        with transaction.atomic():
                order=Order(amount=info['payment'],note=info['note'])
                OrderItem.objects.bulk_create([OrderItem(order=order,menu=k,quantity=v) for k,v in reduced_orders.items()])
                order.save()

        return JsonResponse({'status':'success','uuid':str(order.pk),'time':str(datetime.now())}, status=201)


    except Exception as e:
        traceback.print_exc()

        raise Exception(e)








@validate_form()#empty body
def order_handler_get(req: WSGIRequest,data=None,uuid=None):

    if not uuid:
        return JsonResponse({'status':'Not found'}, status=404)
    order_qs=OrderItem.objects.select_related().all().filter(order_id=uuid)
    if not order_qs: # empy querySet object
        return JsonResponse({'status':'Not found'}, status=404)
    else:
        order = order_qs[0]
        response_data=dict()
        response_data['order']=OrderSerializer(order.order).data
        response_data['order']['items']=OrderItemSerializer(order_qs,many=True).data
        return JsonResponse(response_data, safe=False, status=200)





    return HttpResponse('get-handler',status=200)