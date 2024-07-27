from django.db import models
from django.core import validators
from accounts.models import BaseUser

class Address(models.Model):
    area = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.area


class MainValue(models.Model):
    amount = models.PositiveSmallIntegerField(default=50) 

    def __str__(self):
        return f'Default {self.amount}'


class Record(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="records", null=True, blank=True)
    collector = models.ForeignKey(BaseUser, on_delete=models.PROTECT, related_name="collector")
    amount = models.IntegerField(default=0)
    is_refund = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.collector} | {self.customer} | {self.amount}'


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)  
    collect_day = models.PositiveSmallIntegerField(null=True, validators=[
        validators.MinValueValidator(1),
        validators.MaxValueValidator(28),
    ])
    nick_name = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    description = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.address}'
    

class CustomerValue(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="customer_values")
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.customer.name} | {self.amount}'

class Notes(models.Model):
    NOTE_TYPE = (
        (1 , 'ممتنع'),
        (2 , 'صيانه'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="notes")
    note_type = models.IntegerField(choices=NOTE_TYPE)
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.customer}'
    

class Version(models.Model):
    version = models.IntegerField(default=1)

    def update_version(self):
        self.version = self.version + 1
        self.save()

    def __str__(self):
        return f'{self.version}'