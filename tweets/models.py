from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet" , on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    parent = models.ForeignKey("self" , on_delete=models.SET_NULL , null=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.TextField(blank=True , null=True)
    image = models.FileField(upload_to='images/' , blank=True , null=True)
    likes = models.ManyToManyField(User , related_name="tweet_user" , blank=True , through=TweetLike)
    time = models.DateTimeField(auto_now_add=True)


# tweet.likes.add(user)
# tweet.likes.remove(user)
# tweet.likes.set(users)
# TweetLike.objects.create(user= , tweet=)

    class Meta:
        ordering = ['-id']


    # @property
    def is_retweet(self):
        return self.parent != None

    def serialize(self):
        return {
            "id" : self.id,
            "content" : self.content,
            "likes" : 0
        }