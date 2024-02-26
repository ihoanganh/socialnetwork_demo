from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name='feed'),
    path("post/<slug:slug>/", views.post_detail, name='post-detail'),
    
    #Ajax URLS
    path("create_post/", views.create_post, name='create_post'),
    path("like_post/", views.like_post, name='like_post'),
    path("comment_post/", views.comment_on_post, name='comment_post'),
    path("like_comment/", views.like_comment, name='like_comment'),
    path("reply_comment/", views.reply_comment, name='reply_comment'),
    path("delete_comment/", views.delete_comment, name='delete_comment'),
    path("delete_reply/", views.delete_reply, name='delete_reply'),
]
