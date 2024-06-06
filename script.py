import django
import os
import sys
from django_seed import Seed
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from customers.models import Customer, Address

# Set locale to Arabic
faker = Faker('ar')

# Your seeding logic here
seeder = Seed.seeder()
for _ in range(10):
    seeder.add_entity(Customer, 1, {
        'name': faker.name(),
        # address mut be created object
        'address': Address.objects.get(id=faker.random_int(min=1, max=10)),
        'amount': faker.random_int(min=1, max=100),
        'collect_day': 1,
        'nick_name': faker.name(),
        'phone': faker.phone_number(),
        'description': faker.text(),
        'is_active': True
    })

seeder.execute()


