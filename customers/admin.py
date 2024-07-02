from django.contrib import admin
from customers.models import Customer, Record, Address, MainValue, Notes

class Pagination(admin.ModelAdmin):
    list_per_page = 50  

admin.site.register(Customer, Pagination)
admin.site.register(Record, Pagination)
admin.site.register(Address, Pagination)
admin.site.register(MainValue)
admin.site.register(Notes, Pagination)