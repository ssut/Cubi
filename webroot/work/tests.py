from django.test import TestCase

# Custom user model
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from member.models import *
from work.models import *
from work.crawl import crawl_daumleague

class Crawl(TestCase):
    def daumleague(self):
        user = CubiUser.objects.get(id=1)
        comic_number = '1549'

        crawl_daumleague(comic_number, user)