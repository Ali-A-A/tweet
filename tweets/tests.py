from django.test import TestCase

from .models import Tweet
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
import json

User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='def' , password='somepass')
        self.user2 = User.objects.create_user(username='def2' , password='somepass')
        Tweet.objects.create(content="tweet1" , user=self.user)
        Tweet.objects.create(content="tweet2" , user=self.user)
        Tweet.objects.create(content="tweet3" , user=self.user)
        Tweet.objects.create(content="tweet4" , user=self.user2)


    def test_tweet_create(self):
        tweet = Tweet.objects.create(content="tweet5" , user=self.user)
        self.assertEqual(tweet.id , 5)
        self.assertEqual(tweet.content , "tweet5")

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username , password='somepass')
        return client

    def test_tweet_list_api(self):
        client = self.get_client()
        data = client.get('/tweets/')
        self.assertEqual(data.status_code , 200)
        self.assertEqual(len(data.json()) , 4)

    def test_tweet_action_like(self):
        client = self.get_client()
        data = client.post('/tweet/action' , {"id" : 1 , "action" : "like"})
        self.assertEqual(data.status_code , 200)
        self.assertEqual(data.json().get('likes') , 1)

    def test_tweet_action_unlike(self):
        client = self.get_client()
        client.post('/tweet/action' , {"id" : 1 , "action" : "like"})
        data = client.post('/tweet/action' , {"id" : 1 , "action" : "unlike"})
        self.assertEqual(data.status_code , 200)
        self.assertEqual(data.json().get('likes') , 0)

    def test_tweet_action_retweet(self):
        client = self.get_client()
        data = client.post('/tweet/action' , {"id" : 1 , "action" : "retweet" , "content" : "tweet1"})
        self.assertEqual(data.status_code , 201)
        self.assertEqual(data.json().get('content') , 'tweet1')
        self.assertEqual(data.json().get('likes') , 0)
        self.assertEqual(data.json().get('id') , 5)

    def test_tweet_create_api_view(self):
        data = {"content" : "My tweet"}
        res = self.get_client().post('/create-tweet' , data=data)
        self.assertEqual(res.status_code , 201)
        self.assertEqual(res.json().get('id') , 5)

    def test_unauthenticated_user(self):
        client = APIClient()
        data = client.post('/tweet/action' , {"id" : 1 , "action" : "like"})
        self.assertEqual(data.status_code , 403)
        self.assertEqual(data.json().get('detail') , 'Authentication credentials were not provided.')

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        data = client.post("/tweet/delete/1")
        self.assertEqual(data.status_code , 200)
        self.assertEqual(data.json().get('message') , 'Tweet Deleted Successfully')
        data = client.post("/tweet/delete/1")
        self.assertEqual(data.status_code , 404)
        data = client.post("/tweet/delete/4")
        self.assertEqual(data.status_code , 403)