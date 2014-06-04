#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
import json
from member.models import TinicubeUser

class MemberAPITestCase(TestCase):
    def setUp(self):
        pass
    def test_signup_api(self):
        c = Client()
        signup_res = c.post("/api/signup/",{
                "email":"user1@email.com",
                "password":"pass1",
                "nickname":"testnick1"
                })
        #print signup_res
        users = TinicubeUser.objects.filter(nickname="testnick1")[0]
        self.assertEqual(users.nickname,"testnick1")
