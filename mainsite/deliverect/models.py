from django.db import models
from datetime import datetime
import uuid




class Menu(models.Model):
    description = models.CharField(default='',max_length=240,blank=True, null=False)
    price = models.FloatField(default=0 , blank=False)
    quantity = models.IntegerField(default=0 )
    uuid=models.UUIDField(default=uuid.uuid4, blank=False, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=False, editable=False)

    class Meta:
        ordering = ["-created_at"] #LIFO - Last in first out







    def __str__(self):
        return f'{{ id: {self.id}, uuid: {self.uuid} , price: {self.price},  quantity: {self.quantity}, description: {self.description}, created:{self.created_at} }}'


    def __repr__(self):
        return f'Menu(id: {self.id}, uuid: {self.uuid} , price: {self.price},  quantity: {self.quantity}, description: {self.description}, created:{self.created_at})'


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)