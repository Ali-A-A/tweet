from django.contrib import admin
from django.urls import path , include
from tweets.views import home_view , tweet_detail , tweet_list_view , tweet_create , tweet_delete , tweet_action , tweets_detail_view , tweets_list_view , tweets_profile_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home_view),
    path('list' , tweets_list_view),
    path('<int:tweet_id>', tweets_detail_view),
    path('profile/<str:username>' , tweets_profile_view),
    path('create-tweet' , tweet_create),
    path('tweets/' , tweet_list_view),
    path('tweet/' , include("tweets.urls")),
    path('react/' , TemplateView.as_view(template_name='react.html'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)