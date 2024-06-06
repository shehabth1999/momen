from django.db import models
from django.core import validators
from accounts.models import BaseUser

class Address(models.Model):
    area = models.CharField(max_length=50)

    def __str__(self):
        return self.area


class MainValue(models.Model):
    amount = models.PositiveSmallIntegerField(default=50) 

    def __str__(self):
        return f'Default {self.amount}'


class Record(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, related_name="records", null=True, blank=True)
    collector = models.ForeignKey(BaseUser, on_delete=models.PROTECT, related_name="collector")
    amount = models.IntegerField(default=0)
    is_refund = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.collector} | {self.customer} | {self.amount}'


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)  
    amount = models.PositiveIntegerField(default=0)
    collect_day = models.PositiveSmallIntegerField(null=True, validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(28),
    ])
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null= True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.address}'
