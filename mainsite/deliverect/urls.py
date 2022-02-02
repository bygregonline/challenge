from django.urls import path,re_path
from .views import (get_info,
                    menu_handler,
                    get_process,
                    testing_error)

urlpatterns = [
    path('api/v1/info', get_info,name='get_info'), #just for development purpose
    path('api/v1/error', testing_error ,name='testing-error'), #just for development purpose
    path('api/v1/ps', get_process, name='get_process'),
    path('api/v1/menu', menu_handler,name='menu_handler'),
    path('api/v1/menu/', menu_handler,name='menu_handler/'),
    path('api/v1/menu/<uuid:uuid>', menu_handler, name='menu_handler/uuid'),


]



