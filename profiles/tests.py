from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework.test import APIClient


User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='def' , password='somepass')
        self.user2 = User.objects.create_user(username='def2' , password='somepass')

    def test_followers(self):
        # profile1 = Profile.objects.get(user__id=self.user.id)
        profile1 = self.user.profile
        profile1.followers.add(self.user2)
        self.assertEqual(profile1.followers.first() , self.user2)
        self.assertEqual(self.user2.following.first() , profile1)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username , password='somepass')
        return client

    def test_api_followers(self):
        client = self.get_client()
        data = client.post('/profiles/def2/follow/' , {"action" : "follow"})
        self.assertEqual(data.status_code , 200)
        self.assertEqual(data.json().get("count") , 1)
        self.assertEqual(self.user.following.all().count() , 1)
        self.assertEqual(self.user.following.all().first() , self.user2.profile)
        data = client.post('/profiles/def2/follow/' , {"action" : "unfollow"})
        self.assertEqual(self.user.following.all().count() , 0)
