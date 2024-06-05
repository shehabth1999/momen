from django.db import models
from django.core import validators

class Address(models.Model):
    city = models.CharField(max_length=50)


class MainValue(models.Model):
    amount = models.PositiveSmallIntegerField(default=50) 


class Record(models.Model):
    amount = models.PositiveSmallIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    collect_day = models.PositiveSmallIntegerField(null=True, validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(28),
    ])
    is_active = models.BooleanField(default=True)
    amount = models.PositiveIntegerField(default=0)
