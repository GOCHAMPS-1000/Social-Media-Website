# social_media/core/urls.py
from django.urls import path
from .views import (
    home, signup, signin, logout,
    account_settings, upload_post,
    post_feed, like_post,
    profile, follow_user,
    unfollow_user, search_user,
    user_suggestions, add_comment,
    notifications, mark_as_read,
)

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('settings/', account_settings, name='account_settings'),
    path('upload/', upload_post, name='upload_post'),
    path('feed/', post_feed, name='post_feed'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('profile/<str:username>/', profile, name='profile'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
    path('search/', search_user, name='search_user'),
    path('suggestions/', user_suggestions, name='user_suggestions'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/mark/<int:notification_id>/', mark_as_read, name='mark_as_read'),
]