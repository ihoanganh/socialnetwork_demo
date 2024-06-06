from django.urls import path, include

from core import views
from rest_framework.routers import DefaultRouter


# app_name = "core"
# router = DefaultRouter()
# router.register(r'api/posts', views.PostViewSet, basename="post")
# router.register(r'api/user', views.UserViewSet, basename="user")

urlpatterns = [
    path("", views.index, name='feed'),
    path("core/post/<slug:slug>/", views.post_detail, name='post-detail'),
    
    
    # Chat 
    
    path("core/inbox/", views.inbox, name="inbox"),
    path("core/inbox/<username>/", views.inbox_detail, name="inbox_detail"),
    
    
    # Group CHat
    path("core/group-inbox/", views.group_inbox, name="group_inbox"),
    path("core/create-group-chat/", views.create_group_chat, name="create_group_chat"),
    path("core/group-inbox/<slug:slug>/", views.group_inbox_detail, name="group_inbox_detail"),
    

    # Join & leave Group
    path("core/join-group-page/<slug:slug>/", views.join_group_chat_page, name="join_group_chat_page"),
    path("core/join-group-chat/<slug:slug>/", views.join_group_chat, name="join_group_chat"),
    path("core/leave-group/<slug:slug>/", views.leave_group_chat, name="leave_group_chat"),
    
    # Search
    path('search/', views.search_users, name='search_users'),
    
    
    # Groups, pages
    path('core/groups/', views.groups, name='groups'),
    path('core/group/<slug:slug>/', views.group_detail, name='group_detail'),
    path('core/groups/create/', views.create_group, name='create_group'),
    path('core/groups/create_post/<slug:group_slug>/', views.create_gr_post, name='create_group_post'),
    path("core/join-group/<slug:slug>/", views.join_group, name="join_group"),
    path("group/<slug:group_slug>/create_post/", views.create_gr_post, name='create_gr_post'),
    path("like_gr_post/", views.like_gr_post, name='like_gr_post'),
    path("comment_gr_post/", views.comment_gr_post, name='comment_gr_post'),
    path("like_gr_comment/", views.like_comment, name='like_gr_comment'),
    path("reply_gr_comment/", views.reply_gr_comment, name='reply_gr_comment'),
    path("delete_gr_comment/", views.delete_comment, name='delete_gr_comment'),
    path("delete_gr_reply/", views.delete_reply, name='delete_gr_reply'),
    path('core/pages/', views.pages, name='pages'),
    path('core/pages/create/', views.create_page, name='create_page'),

    path('core/page/<slug:slug>/', views.page_detail, name='page_detail'),
    
    #Ajax URLS
    path("create_post/", views.create_post, name='create_post'),
    path("delete_post/", views.delete_post, name='delete_post'),
    path("like_post/", views.like_post, name='like_post'),
    path("comment_post/", views.comment_on_post, name='comment_post'),
    path("like_comment/", views.like_comment, name='like_comment'),
    path("reply_comment/", views.reply_comment, name='reply_comment'),
    path("delete_comment/", views.delete_comment, name='delete_comment'),
    path("delete_reply/", views.delete_reply, name='delete_reply'),
    path("add_friend/", views.add_friend, name='add_friend'),
    path("accept_friend_request/", views.accept_friend_request, name='accept_friend_request'),
    path("reject_friend_request/", views.reject_friend_request, name='reject_friend_request'),
    path("unfriend/", views.unfriend, name='unfriend'),
    path("block_user/", views.block_user, name='block_user'),
    
    # Load more post
    path('load_more_posts/', views.load_more_posts, name='load_more_posts'),


    # api - rest framework
    # path("", include(router.urls)),
]
