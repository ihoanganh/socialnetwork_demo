
from django.contrib import admin
from core.models import PagePost,Group, GroupPost, Page, Post, Gallery, ReplyComment,Friend, FriendRequest, Comment, Notification, ChatMessage, GroupChatMessage, GroupChat

class GalleryAdminTab(admin.TabularInline):
    model = Gallery

class ReplyCommnentTabAdmin(admin.TabularInline):
    model = ReplyComment
     
    
class PostAdmin(admin.ModelAdmin):
    inlines = [GalleryAdminTab]
    list_editable = ['active']
    list_display = ['thumbnail', 'user', 'title', 'visibility', 'active']
    prepopulated_fields = {"slug":("title", )}

class GalleryAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['thumbnail', 'post', 'active']
    
    
class FriendRequestAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['sender', 'receiver', 'status']

class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend']
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'group_post', 'comment', 'date', 'active','id')
    list_filter = ('active', 'date')
    search_fields = ('user__username', 'comment')

class ReplyCommnentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_comment_content', 'active']  
    def get_comment_content(self, obj):
        return obj.comment.comment
    
    get_comment_content.short_description = 'Comment Content'
    
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'sender', 'post', 'comment', 'is_read']    
    
class GroupPostAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['thumbnail', 'user', 'title', 'visibility', 'active']
    prepopulated_fields = {"slug":("title", )} 

class GroupAdmin(admin.ModelAdmin):
    # inlines = [GroupPostTabAdmin]
    list_editable = ['user', 'name', 'visibility']
    list_display = ['thumbnail', 'user', 'name','visibility']
    prepopulated_fields = {'slug':('name',)}
    
class PageAdmin(admin.ModelAdmin):
    list_editable = ['user', 'name', 'visibility']
    list_display = ['thumbnail', 'user', 'name','visibility']
    prepopulated_fields = {'slug':('name',)}
    
class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['message']
    list_display = ['chat_sender', 'chat_receiver', 'message','date', 'is_read']

class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'description' ,'host','active']
    prepopulated_fields = {"slug": ("name", )}
    

class GroupChatMessageAdmin(admin.ModelAdmin):
    list_display = ['groupchat', 'sender', 'message' ,'is_read','date']


admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommnentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GroupPost, GroupPostAdmin)
admin.site.register(PagePost)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(GroupChatMessage, GroupChatMessageAdmin)
admin.site.register(GroupChat, GroupChatAdmin)