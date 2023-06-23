# -*- coding: utf-8 -*-

import django
import os 
import sys

from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","server.settings")
django.setup()

from account.models import User

users = User.objects.all()

'''
for user in users:
    # clear the suggestion list
    user.people_you_may_know.clear()
    print('Find friends for:',user)

    for friend in user.friends.all():
        if user not in friend.friends.all():
            print('suggest me')
        
        print('Already friend with:',friend)
    print('')
'''

for user in users:
    user.people_you_may_know.clear()
    print('Find friends for:',user)
    for friend in user.friends.all():
        # every friendship
        print('Is friend with:',friend)

        for friendsfriend in friend.friends.all():
            if friendsfriend not in user.friends.all() and friendsfriend != user:
                print('Suggest:',friendsfriend)
                user.people_you_may_know.add(friendsfriend)
    print()

