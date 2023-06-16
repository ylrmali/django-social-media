from django.urls import path
from mainapp.views import *

# name = 'mainapp'

# url define and which function will work with this url
urlpatterns = [
    path('', home, name='home'),
    path('explore/', explore, name='explore'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/ask/create/', post_create, name='post-create'),
    path('like/<int:post_id>/', like, name='like'),
    path('follow/<int:current_user_id>/<int:target_user_id>/', follow, name='follow'),
    path('unfollow/<int:current_user_id>/<int:target_user_id>/', unfollow, name='unfollow'),
    path('check/', check, name='check'),
    path('like-control/<int:post_id>/<user_id>/', like_control, name='like_control'),
    path('comment_count/<int:post_id>/', post_comment, name='post_comment'),
    path('comment_like/<int:comment_id>/', comment_like, name='comment_like'),
    path('comment_like_control/<int:comment_id>/', comment_like_control, name='comment_like_control'),
    path('search/<str:argument>/', search, name='search'),
    path('edit/<int:user_id>/', profile_edit, name='edit_profile'),
    path('notification/', notification, name='notification'),
    path('ignore/<int:noti_id>/', ignore_follower, name='ignore'),
    path('accept/<int:current_user_id>/<int:target_user_id>/<int:noti_id>/', accept_follower, name='accept'),
    path('refollow/<int:current_user_id>/<int:target_user_id>/<int:noti_id>/', refollow, name='refollow'),
    path('message/<int:sender>/<int:reciever>/', message, name='message'),
    path('message-box/<int:current_user>/', message_box, name='message_box'),
]

