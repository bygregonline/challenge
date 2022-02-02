from django.http import Http404, JsonResponse, HttpResponse,HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from pyvalid import accepts, returns
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
import platform
import logging
from .utils import validate_form
from .models import Menu
from .serializers import ModelSerializer
from datetime import datetime
import subprocess
from django.shortcuts import get_object_or_404


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
