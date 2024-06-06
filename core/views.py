from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.http import JsonResponse
from django.utils.timesince import timesince
import shortuuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, Q
from django.core.paginator import Paginator


from core.models import Post,GroupPost, Comment, ReplyComment, Friend, FriendRequest, Notification, ChatMessage, GroupChat, GroupChatMessage, Group, Page
from userauths.models import User, Profile
from core.forms import *
from core.serializers import *
from rest_framework import generics, viewsets

#Notification keys
noti_new_like = 'New Like' #models
noti_new_follower = 'New Follower'
noti_friend_request = 'Friend Request'
noti_new_comment = 'New Comment'
noti_comment_liked = 'Comment Liked'
noti_comment_replied = 'Comment Replied'
noti_friend_request_accepted = 'Friend Request Accept'



def send_noti(user, sender, post, comment, notification_type):
    notification = Notification.objects.create(
        user = user,
        sender = sender,
        post = post,
        comment = comment,
        notification_type = notification_type,
    )
    return notification



@login_required
def index(request):
    posts = Post.objects.filter(active=True, visibility="Everyone").order_by("-id")
    # posts = Post.objects.all()
    paginator = Paginator(posts, 3)  
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    groupchat = GroupChat.objects.filter(members__in=User.objects.filter(pk=request.user.pk), active=True)

    context = {
        "posts":posts,
        'groupchat': groupchat
    }
    return render(request, "core/index.html", context)

@login_required
def post_detail(request, slug):
    post = Post.objects.get(slug=slug, active=True, visibility="Everyone")
    context = {
        "p":post
    }
    return render(request, "core/post-detail.html", context)


@csrf_exempt
def create_post(request):
    
    if request.method == "POST": #<from method="POST">
        title = request.POST.get("post-caption") #<input type="text" name="post-caption">
        visibility = request.POST.get("visibility")
        image = request.FILES.get("post-thumbnail")
        

        uuid_key = shortuuid.uuid() 
        uniqueid = uuid_key[:4]
        
        post = Post(
            title=title,
            image=image,
            visibility=visibility,
            user=request.user,
            slug=slugify(title) + '-' + str(uniqueid.lower())
        )
        if image:  # Kiểm tra xem có tệp ảnh được gửi không
            post.image = image
        post.save()
        
        return JsonResponse({'post' :
            {"title":post.title if post.title else "",
            "image":post.image.url if post.image else "",
            "full_name":post.user.profile.full_name,
            "profile_image":post.user.profile.image.url,
            "date":timesince(post.date),
            "id":post.id}
        }
        )
        return JsonResponse({"error":"Title does not exists"})
    
    return JsonResponse({"data":"sent"})    

@csrf_exempt
def create_gr_post(request,group_slug):
    if request.method == "POST":
        title = request.POST.get("gr-post-caption")
        visibility = request.POST.get("gr-visibility")
        image = request.FILES.get("gr-post-thumbnail")

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]



        # Lấy thông tin group từ slug
        try:
            group = Group.objects.get(slug=group_slug)  # Sử dụng get thay vì filter
        except Group.DoesNotExist:
            return JsonResponse({"error": "Group not found"}, status=404)

        gr_post = GroupPost(
            title=title,
            visibility=visibility,
            user=request.user,
            group=group,
            slug=slugify(title) + '-' + str(uniqueid.lower())
        )

        if image:
            gr_post.image = image

        gr_post.save()

        return JsonResponse({'post': {
            "title": gr_post.title,
            "image": gr_post.image.url if gr_post.image else "",
            "full_name": gr_post.user.profile.full_name,
            "profile_image": gr_post.user.profile.image.url,
            "date": timesince(gr_post.date),
            "id": gr_post.id,
            "group": {
                "slug": gr_post.slug
            }
        }})

    return JsonResponse({"data":"sent"})

def delete_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    post.delete()
    
    data = {
        "bool": True
    }
    return JsonResponse({"data":data})

def like_post(request):
    id = request.GET['id'] #/like-post/?id=1
    post = Post.objects.get(id=id)
    user = request.user
    bool = False
    
    if user in post.likes.all(): #vi like lien ket nhieu nhieu voi user nen phai check user
        post.likes.remove(user) # add vs remove ko can post_save
        bool = False
        
        
        
    else:
        post.likes.add(user)
        bool = True 
        
        #send noti
        if post.user != request.user:
            send_noti(post.user, user, post, None, noti_new_like)
        
    data = {
        'bool':bool,
        "likes":post.likes.all().count()
        
    }
    return JsonResponse({"data":data})

def like_gr_post(request):
    id = request.GET['id'] 
    gr_post = GroupPost.objects.get(id=id)
    user = request.user
    bool = False
    
    if user in gr_post.likes.all(): #vi like lien ket nhieu nhieu voi user nen phai check user
        gr_post.likes.remove(user) # add vs remove ko can post_save
        bool = False
              
    else:
        gr_post.likes.add(user)
        bool = True 
        
       
        
    data = {
        'bool':bool,
        "likes":gr_post.likes.all().count()
        
    }
    return JsonResponse({"data":data})

def comment_on_post(request):
    id = request.GET['id']
    comment = request.GET['comment'] # "comment"
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user
    
    new_comment = Comment.objects.create(
        post = post,
        comment = comment,
        user = user,
    )
    
    if new_comment.user != post.user:
        send_noti(post.user, user, post, new_comment, noti_new_comment)
    data = {
        "bool": True,
        "comment": new_comment.comment,
        "profile_image": new_comment.user.profile.image.url,
        "date": timesince(new_comment.date),
        "comment_id": new_comment.id,
        "post_id": new_comment.post.id,
        "comment_count": comment_count + int(1),
    }
    
    return JsonResponse({"data":data})

def comment_gr_post(request):
    id = request.GET['id']
    comment = request.GET['comment'] # "comment"
    gr_post = GroupPost.objects.get(id=id)
    comment_count = Comment.objects.filter(group_post=gr_post).count()
    user = request.user
    
    new_comment = Comment.objects.create(
        group_post = gr_post,
        comment = comment,
        user = user,
    )
    
    if new_comment.user != gr_post.user:
        send_noti(gr_post.user, user, gr_post, new_comment, noti_new_comment)
    data = {
        "bool": True,
        "comment": new_comment.comment,
        "profile_image": new_comment.user.profile.image.url,
        "date": timesince(new_comment.date),
        "comment_id": new_comment.id,
        "gr_post_id": new_comment.group_post.id,
        "comment_count": comment_count + int(1),
    }
    
    return JsonResponse({"data":data}) 

def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False
    
    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True
        
        if comment.user != user:
            send_noti(comment.user, user, comment.post, comment, noti_comment_liked)
        
    data = {
        "bool": bool,
        "likes":comment.likes.all().count(),
    }
    
    return JsonResponse({"data":data})



def reply_comment(request):
    id = request.GET['id']
    reply = request.GET['reply']
    
    comment = Comment.objects.get(id=id)
    user = request.user
    
    new_reply = ReplyComment.objects.create(
        comment = comment,
        user = user,
        reply = reply,
    )
    if comment.user != user:
        send_noti(comment.user, user, comment.post, comment, noti_comment_replied)
        
    data = {
        "bool": True,
        "reply": new_reply.reply,
        "profile_image": new_reply.user.profile.image.url,
        "date": timesince(new_reply.date),
        "reply_id": new_reply.id,
        "post_id": new_reply.comment.post.id,
    }
    return JsonResponse({"data":data})

def reply_gr_comment(request):
    id = request.GET['id']
    reply = request.GET['reply']
    
    comment = Comment.objects.get(id=id)
    user = request.user
    
    new_reply = ReplyComment.objects.create(
        comment = comment,
        user = user,
        reply = reply,
    )

    data = {
        "bool": True,
        "reply": new_reply.reply,
        "profile_image": new_reply.user.profile.image.url,
        "date": timesince(new_reply.date),
        "reply_id": new_reply.id,
        "gr_post_id": new_reply.comment.group_post.id,
    }
    return JsonResponse({"data":data})
    

def delete_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    comment.delete()
    
    data = {
        "bool": True
    }
    return JsonResponse({"data":data})


def delete_reply(request):
    id = request.GET['id']
    reply = ReplyComment.objects.get(id=id)
    reply.delete()
    
    data = {
        "bool": True
    }
    return JsonResponse({"data":data})

def add_friend(request):
    sender = request.user
    receiver_id = request.GET['id']
    bool = False
    
    if sender.id == int(receiver_id):
        return JsonResponse({"error":"You cannot send a friend request to yourself"})
    
    receiver = User.objects.get(id=receiver_id)
    
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        return JsonResponse({"error":"Cancelled", "bool":bool})

    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True
        
        send_noti(receiver, sender, None, None, noti_friend_request)
        
        
        return JsonResponse({"success":"Sent", "bool":bool})

def accept_friend_request(request):
    id = request.GET['id']
    
    receiver = request.user #dung
    sender = User.objects.get(id=id) #ha
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
    
    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)
    
    friend_request.delete()
    
    send_noti(receiver, sender, None, None, noti_friend_request_accepted)
    
    data = {
        'message': "Accepted",
        'bool': True,
    }
    
    return JsonResponse({'data':data})

def reject_friend_request(request):
    id = request.GET['id']
    
    receiver = request.user #dung
    sender = User.objects.get(id=id) #ha
    
    friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
    
    friend_request.delete()
    
    data = {
        'message': "Rejected",
        'bool': True,
    }
    
    return JsonResponse({'data':data})


def unfriend(request):
    sender = request.user 
    friend_id = request.GET['id']
    bool = False
    
    if sender.id == int(friend_id):
        return JsonResponse({"error":"You cannot unfriend yourself"})
    
    my_friend = User.objects.get(id=friend_id)
    
    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        bool = True
        return JsonResponse({"success":"Unfriend Successfully.", "bool":bool})


@login_required
def inbox(request):
    user_id = request.user
    groupchat = GroupChat.objects.filter(members__in=User.objects.filter(pk=request.user.pk), active=True)

    chat_message = ChatMessage.objects.filter(
        id__in = Subquery(
            User.objects.filter(
                Q(chat_sender__chat_receiver = user_id)  |
                Q(chat_receiver__chat_sender = user_id)
            ).distinct().annotate(
                last_msg = Subquery(
                    ChatMessage.objects.filter(
                        Q(chat_sender=OuterRef("id"), chat_receiver=user_id) |
                        Q(chat_receiver=OuterRef("id"), chat_sender=user_id)
                    ).order_by("-id")[:1].values_list("id", flat=True)
                )
            ).values_list("last_msg", flat=True).order_by("-id")
        )
    ).order_by("-id")
    
    context = {
        "chat_message": chat_message,
        'groupchat':groupchat
    }
    
    return render(request, "chat/inbox.html", context)


def inbox_detail(request, username):
    user_id = request.user
    
    message_list = ChatMessage.objects.filter(
        id__in = Subquery(
            User.objects.filter(
                Q(chat_sender__chat_receiver = user_id)  |
                Q(chat_receiver__chat_sender = user_id)
            ).distinct().annotate(
                last_msg = Subquery(
                    ChatMessage.objects.filter(
                        Q(chat_sender=OuterRef("id"), chat_receiver=user_id) |
                        Q(chat_receiver=OuterRef("id"), chat_sender=user_id)
                    ).order_by("-id")[:1].values_list("id", flat=True)
                )
            ).values_list("last_msg", flat=True).order_by("-id")
        )
    ).order_by("-id")
    
    chat_sender = request.user
    chat_receiver = User.objects.get(username=username)
    receiver_detail = User.objects.get(username=username)

    message_detail = ChatMessage.objects.filter(
        Q(chat_sender=chat_sender, chat_receiver=chat_receiver) | Q(chat_sender=chat_receiver, chat_receiver=chat_sender)
    ).order_by("date")
    
    message_detail.update(is_read=True)
    
    if message_detail:
        r = message_detail.first()
        chat_receiver = User.objects.get(username=r.chat_receiver)
    else:
        chat_receiver = User.objects.get(username=username)
    
    context = {
        "message_detail": message_detail,
        "chat_receiver": chat_receiver,
        "chat_sender": chat_sender,
        "receiver_detail": receiver_detail,
        "message_list": message_list,
    }
    
    return render(request, "chat/inbox_detail.html", context)

def block_user(request):
    id = request.GET['id']
    user = request.user
    friend = User.objects.get(id=id)
    
    if user.id == friend.id:
        return JsonResponse({"error": "You cannot block yourself"})
    
    if friend in user.profile.friends.all():
        user.profile.blocked.add(friend)
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
    else:
        return JsonResponse({"error": "You cannot block someone that is not your friend"})
    
    return JsonResponse({"success": "User Blocked"})

def load_more_posts(request):
    all_posts = Post.objects.filter(active=True, visibility="Everyone").order_by('-id')

    # Paginate the posts
    paginator = Paginator(all_posts, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    posts_data = []
    for post in page_obj:
        post_data = {
            'title': post.title,
            'profile_image': post.user.profile.image.url,
            'full_name': post.user.profile.full_name,
            'image_url': post.image.url if post.image else None,
            'video': post.video.url if post.video else None,
            'id': post.id,
            'id': post.id,
            'likes': post.likes.count(),
            'slug': post.slug,
            'views': post.views,
            'date': timesince(post.date),
        }
        posts_data.append(post_data)

    return JsonResponse({'posts': posts_data})



@login_required
def group_inbox(request):
    groupchat = GroupChat.objects.filter(members__in=User.objects.filter(pk=request.user.pk), active=True)
    print("groupchat =============", groupchat)
    context = {
        'groupchat': groupchat,
    }
    return render(request, 'chat/group_inbox.html', context)


@login_required
def group_inbox_detail(request, slug):
    groupchat_list = GroupChat.objects.filter(members__in=User.objects.filter(pk=request.user.pk), active=True)
    groupchat = GroupChat.objects.filter(slug=slug, active=True).first()
    group_messages = GroupChatMessage.objects.filter(groupchat=groupchat).order_by("id")

    if request.user not in groupchat.members.all():
        return redirect("core:join_group_chat_page", groupchat.slug)
    

    context = {
        'groupchat': groupchat,
        'group_name': groupchat.slug,
        'group_messages': group_messages,
        'groupchat_list': groupchat_list,
    }
    return render(request, 'chat/group_inbox_detail.html', context)

def join_group_chat_page(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    context = {
        'groupchat': groupchat,
    }
    return render(request, 'chat/join_group_chat_page.html', context)

@csrf_exempt
def create_group_chat(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('group-chat-name')
        description = request.POST.get('group-chat-description')
        
        
        # Tạo đối tượng Group và lưu vào database
        group_chat = GroupChat.objects.create(host=user, name=name, description=description)
        members = request.POST.getlist('members[]')
        for member in members:
            friend = User.objects.get(pk=member)
            group_chat.members.add(friend)
            
        group_chat.members.add(user)
        
        return redirect('core:group_inbox')
    friends = User.objects.all()
    
    return render(request, 'chat/create_group_chat.html', {'friends': friends})
    
    
def join_group_chat(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    if request.user in groupchat.members.all():
        return redirect("core:group_inbox_detail", groupchat.slug)
    
    groupchat.members.add(request.user)
    return redirect("core:group_inbox_detail", groupchat.slug)


def leave_group_chat(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    if request.user in groupchat.members.all():
        groupchat.members.remove(request.user)
        return redirect("core:join_group_chat_page", groupchat.slug)

    return redirect("core:join_group_chat_page", groupchat.slug)

def search_users(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query) | User.objects.filter(full_name__icontains=query)

        users_data = []
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                profile_image = profile.image.url
                full_name = profile.full_name
            except Profile.DoesNotExist:
                profile_image = None
                full_name = None

            user_data = {
                'username': user.username,
                'full_name': full_name,
                'email': user.email,
                'profile_image': profile_image,
            }
            users_data.append(user_data)
    else:
        users_data = []
    return JsonResponse({'users': users_data})


def groups(request):
    groups = Group.objects.filter(visibility='Everyone').order_by('-id')
    context = {
        'groups':groups
    }
    return render(request, 'core/groups.html', context)

def group_detail(request,slug):
    group = Group.objects.get(slug=slug, active =True, visibility='Everyone')
    group_post = GroupPost.objects.filter(active=True).order_by("-id")
    context = {
        'g':group,
        'gp':group_post,
    }
    return render(request, 'core/group-detail.html',context)

def join_group(request, slug):
    group = Group.objects.get(slug=slug, active=True)
    
    if request.user in group.member.all():
        return redirect("core:group_detail", group.slug)
    
    group.member.add(request.user)
    return redirect("core:group_detail", group.slug)
@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('group-name')
        description = request.POST.get('group-description')
        visibility = request.POST.get('group-visibility')
        
        # Tạo đối tượng Group và lưu vào database
        group = Group.objects.create(user=user, name=name, decription=description, visibility=visibility)
        
        group.member.add(user)
        
        return redirect('core:groups')
    
    return render(request, 'core/create-group.html')


def pages(request):
    pages = Page.objects.filter(active =True).order_by('-id')
    top_pages = Page.objects.all()
    context = {
        'pages':pages,
        'top_pages':top_pages
    }
    return render(request, 'core/pages.html', context)

@csrf_exempt
def create_page(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('page-name')
        description = request.POST.get('page-description')
        
        # Tạo đối tượng Page và lưu vào database
        page = Page.objects.create(user=user, name=name, decription=description)
        
        page.follower.add(request.user)
        return redirect('core:pages')
    
    return render(request, 'core/create-page.html')

def page_detail(request, slug):
    page = Page.objects.get(slug=slug, active=True)
    context = {
        'p':page
    }
    return render(request, 'core/page-detail.html', context)

# class PostList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
# class PostRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
    
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer