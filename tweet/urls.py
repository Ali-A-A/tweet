from django.contrib import admin
from django.urls import path , include , re_path
from tweets.views import home_view , tweet_detail , tweet_list_view , tweet_create , tweet_delete , tweet_action , tweets_detail_view , tweets_list_view , tweets_profile_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from accounts.views import login_view , register_view , logout_view
from profiles.views import profile_view , profile_updata_view , user_follow , tweet_feed_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home_view),
    path('list' , tweets_list_view),
    path('<int:tweet_id>', tweets_detail_view),
    path('create-tweet' , tweet_create),
    path('tweets/' , tweet_list_view),
    path('tweet/' , include("tweets.urls")),
    path('profiles/<str:username>/follow/' , user_follow),
    path('profiles/feed/' , tweet_feed_view),
    path('login' , login_view),
    path('register' , register_view),
    path('profiles/update' , profile_updata_view),
    re_path(r'^profiles/?' , profile_view),
    path('logout' , logout_view),
    path('react/' , TemplateView.as_view(template_name='react.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)