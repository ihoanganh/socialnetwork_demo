from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from core.models import Post, FriendRequest
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from userauths.models import Profile, User

def RegisterView(request):
    
    # if request.user.is_authenticated:
    #     messages.warning(request, "You are registered!")
    #     return redirect('core:feed')
    
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        
        user = authenticate(email=email, password=password)
        login(request, user)
        
        
        profile = Profile.objects.get(user=request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()
        
        messages.success(request, f"Hi {full_name}. You created account successfully.")
        return redirect('core:feed')
    
    context = {
        'form':form
    }
    return render(request, 'userauths/sign-up.html', context)

def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already login!")
        return redirect('core:feed')
        
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
    
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.warning(request, "You are logged in!")
                return redirect('core:feed')
            else:
                messages.error(request, "Username or password does not match")
                return redirect('userauths:sign-up')
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('userauths:sign-up')
            
    return HttpResponseRedirect("/userauths/sign-in/")


def LogoutView(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect("userauths:sign-up")


@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user).order_by("-id")
    
    context = {
        "profile": profile,
        "posts": posts,
    }
    
    return render(request, "userauths/my-profile.html", context)

@login_required
def friend_profile(request, username):
    profile = Profile.objects.get(user__username=username)
    if request.user.profile == profile:
        redirect("userauths:my-profile")
    posts = Post.objects.filter(active=True, user=profile.user).order_by("-id")
    
    bool = False
    bool_friend = False
    
    sender = request.user
    receiver = profile.user
    
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            bool =True
        else:
            bool = False
    except:
        bool = False
        
    context = {
        "profile": profile,
        "posts": posts,
        "bool": bool,
        "posts": posts,
    }
    
    return render(request, "userauths/friend-profile.html", context)


@login_required
def profile_update(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect('userauths:profile-update')
        else:
            messages.error(request, "There was an error updating your profile.")
            print(p_form.errors)
            print(u_form.errors)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'userauths/profile-update.html', context)
