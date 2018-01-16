import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','onlinefleamart1.settings')

import django
django.setup()

import random
from firstapp.models import UserDetails,userHome
from User.models import SellItemInfo
from faker import Faker

fakegen = Faker()

def populate(N=5):

    for entry in range(N):
        fake_username = fakegen.name()
        fake_password = fakegen.lexify(text="??????????", letters="1234567890abcdefghijklmnopqrstABDKLS$%#@")
        fake_email = fakegen.email()
        fake_phone = fakegen.lexify(text="+880-??????????", letters="1234567890")
        fake_adress = fakegen.address()
        fake_url = fakegen.url()
        users = UserDetails.objects.get_or_create(user_name=fake_username,password=fake_password)[0]
        usersDetails = userHome.objects.get_or_create(user_name=users,email=fake_email,phone=fake_phone,address = fake_adress,url = fake_url)[0]

if __name__ == '__main__':
    print("populating the scripts")
    populate(100)
    print("populating complete")
