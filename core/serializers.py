from rest_framework import serializers
from core.models import Post
from userauths.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','image','visibility','active','user','date']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','password', 'full_name', 'username', 'email', 'phone', 'gender']