from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ImageField, FileInput
from userauths.models import Profile, User

from userauths.models import User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}), max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': '','id': '',"placeholder":"Username"}), max_length=100, required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': '','id': '',"placeholder":"Mobile No."}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': '','id': '',"placeholder":"Email Address"}),max_length=100 , required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': '',"placeholder":"Password"}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': '',"placeholder":"Confirm Password"}), required=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2', 'gender', 'phone']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "with-border"
            
            
class ProfileUpdateForm(forms.ModelForm):
    image = ImageField(widget=FileInput)
    
    class Meta:
        model = Profile
        fields = [
            'cover_image' ,
            'image' ,
            'full_name', 
            'bio', 
            'about_me', 
            'phone',
            'gender',
            'relationship',
            'country', 
            'city', 
            'state', 
            'address', 
            'working_at',
            'instagram',
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }