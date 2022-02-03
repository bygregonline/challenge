from django.urls import path,re_path
from .views import (get_info,
                    menu_handler,
                    get_process,
                    testing_error,
                    order_handler)

urlpatterns = [
    path('api/v1/info', get_info,name='get_info'), #just for development purpose
    path('api/v1/error', testing_error ,name='testing-error'), #just for development purpose
    path('api/v1/ps', get_process, name='get_process'),#see whats really appends in the container @real-time @stress-testingg
    path('api/v1/menu', menu_handler,name='menu_handler'),
    path('api/v1/menu/', menu_handler,name='menu_handler/'),
    path('api/v1/menu/<uuid:uuid>', menu_handler, name='menu_handler/uuid'),
    path('api/v1/order', order_handler, name='order_handler'),
    path('api/v1/order/<uuid:uuid>', order_handler, name='order_handler/uuid'),


]



