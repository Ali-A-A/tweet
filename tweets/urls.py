
from django.contrib import admin
from django.urls import path
from tweets.views import tweet_detail , tweet_list_view , tweet_create , tweet_delete , tweet_action

urlpatterns = [
    path('<int:id>' , tweet_detail),
    path('delete/<int:id>' , tweet_delete),
    path('action' , tweet_action)
]
