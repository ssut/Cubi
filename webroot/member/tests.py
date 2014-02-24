#-*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
import json
from member.models import CubiUser

class MemberAPITestCase(TestCase):
    def setUp(self):
        pass
    def test_signup_api(self):
        c = Client()
        signup_res = c.post("/api/signup/",{
                "email":"user1@email.com",
                "password":"pass1",
                "nickname":"nick1"
                })
        users = CubiUser.objects.all()[0]
        self.assertEqual(users.nickname,"nick1")
