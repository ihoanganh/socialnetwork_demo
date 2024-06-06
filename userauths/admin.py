from django.contrib import admin
from userauths.models import User, Profile
# Register your models here.

class UserCustomAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'email', 'gender']
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified']
    list_editable = ['verified']

admin.site.register(User, UserCustomAdmin)
admin.site.register(Profile, ProfileAdmin)