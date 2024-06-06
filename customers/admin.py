from django.contrib import admin
from customers.models import Customer, Record, Address, MainValue


admin.site.register(Customer)
admin.site.register(Record)
admin.site.register(Address)
admin.site.register(MainValue)