from django.apps import AppConfig
from termcolor import colored


class DeliverectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    name = 'deliverect'
    verbose_name = 'deliverect app'
    author = 'Greg Flores'
    date='30/JAN/2022'



    def ready(self):
        print(colored(f'{__name__}  is ready \U0001F448', 'green')) ## little print to know the app  is ready



