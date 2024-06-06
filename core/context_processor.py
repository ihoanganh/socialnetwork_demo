from core.models import FriendRequest, Notification, ChatMessage, GroupChatMessage, GroupChat
from django.db.models import Q, Count, Sum, F, FloatField
from django.db.models import OuterRef, Subquery
from userauths.models import User


def my_context_processor(request):
    try:
        friend_request = FriendRequest.objects.filter(receiver=request.user).order_by("-id")
    except:
        friend_request = None
        
    try:
        notification = Notification.objects.filter(user=request.user).order_by("-id")
    except:
        notification = None
        
    try:
        # chat_message = ChatMessage.objects.filter(user=request.user).order_by("-id")
        user_id = request.user
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
    except:
        chat_message = None
    
    # group chat 
    try:
        # chat_message = ChatMessage.objects.filter(user=request.user).order_by("-id")
        user_id = request.user
        gr_chat_message = GroupChatMessage.objects.filter(
        id__in = Subquery(
            GroupChatMessage.objects.filter(
                Q(group__members__id = user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    GroupChatMessage.objects.filter(
                        group=OuterRef('group'),
                        id__in=GroupChat.objects.filter(members__id=user_id).values_list('groupchatmessage__id', flat=True)
                    ).order_by('-id')[:1].values_list('id', flat=True)
                )
            ).values_list("last_msg", flat=True).order_by("-id")
        )
    ).order_by("-id")
    except:
        gr_chat_message = None
        
        
    return {
        'friend_request':friend_request,
        'notification':notification,
        'chat_message':chat_message,
        'gr_chat_message': gr_chat_message,
        }