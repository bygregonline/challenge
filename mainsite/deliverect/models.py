from django.db import models
from datetime import datetime
import uuid

class Menu(models.Model):
    description = models.CharField(default='',max_length=240,blank=True, null=False)
    price = models.FloatField(default=0 , blank=False)
    quantity = models.IntegerField(default=0 )
    uuid=models.UUIDField(default=uuid.uuid4, blank=False, null=False,primary_key=True)
    created_at = models.DateTimeField(default=datetime.now, blank=False, editable=False)

    class Meta:
        ordering = ["-created_at"] #LIFO - Last in first out



    def __str__(self):
        return f'{{  uuid: {self.uuid} , price: {self.price},  quantity: {self.quantity}, description: {self.description}, created:{self.created_at} }}'


    def __repr__(self):
        return f'Menu(uuid: {self.uuid} , price: {self.price},  quantity: {self.quantity}, description: {self.description}, created:{self.created_at})'


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Order(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, blank=False, null=False, primary_key=True)
    created_at = models.DateTimeField(default=datetime.now, blank=False, editable=False)
    amount = models.FloatField(default=0)
    note = models.CharField(default='',max_length=400,blank=True, null=False)

    class Meta:
        ordering = ["-created_at"] #LIFO - Last in first out


    def __str__(self):
        return f'{{  \nuuid: {self.uuid} \namount: {self.amount} \nnote: {self.note} \ncreated:{self.created_at} }}'

    def __repr__(self):
        return f'Order(uuid: {self.uuid} , amount: {self.amount},  note: {self.note}, created:{self.created_at})'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_menu')
    menu = models.UUIDField(default=uuid.uuid4, blank=False, null=False) #TODO add foreigner key to menu to keep constraint NOT required by the client
    quantity = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=False, editable=False)

    class Meta:
        ordering = ["-created_at"] #LIFO - Last in first out

    def __str__(self):
        return f'{{  \nuuid: {self.uuid} \nmenu: {self.menu} \nquantity: {self.quantity} \ncreated:{self.created_at} }}'

    def __repr__(self):
        return f'OrderItem(uuid: {self.uuid} , menu: {self.menu},  quantity: {self.quantity}, created:{self.created_at})'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)